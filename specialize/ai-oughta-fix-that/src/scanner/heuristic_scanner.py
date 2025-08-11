"""
Heuristic Scanner Module
Implements behavior-based and heuristic malware detection techniques
"""

import os
import re
import struct
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
import logging

from base_scanner import BaseScanner, ScanResult, BaseScannerError

logger = logging.getLogger(__name__)


class HeuristicScannerError(BaseScannerError):
    """Exception specific to heuristic scanner operations"""
    pass


class HeuristicRule:
    """Represents a heuristic detection rule"""
    
    def __init__(self, rule_id: str, name: str, category: str, 
                 weight: float = 1.0, description: str = ""):
        self.rule_id = rule_id
        self.name = name
        self.category = category  # 'behavioral', 'structural', 'anomaly'
        self.weight = weight  # Contribution to overall threat score
        self.description = description
        self.enabled = True
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert rule to dictionary format"""
        return {
            'rule_id': self.rule_id,
            'name': self.name,
            'category': self.category,
            'weight': self.weight,
            'description': self.description,
            'enabled': self.enabled
        }


class HeuristicScanner(BaseScanner):
    """Scanner that uses heuristic and behavioral analysis for malware detection"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("HeuristicScanner", config)
        self.rules: Dict[str, HeuristicRule] = {}
        self.suspicious_apis: Set[str] = set()
        self.suspicious_strings: Set[str] = set()
        self.file_anomaly_thresholds = {
            'entropy_threshold': 7.0,  # High entropy indicates encryption/packing
            'section_count_threshold': 10,  # Unusual number of PE sections
            'import_count_threshold': 100,  # Excessive imports
        }
        
    def _initialize(self) -> None:
        """Initialize the heuristic scanner"""
        self._load_heuristic_rules()
        self._load_suspicious_patterns()
        logger.info(f"Initialized with {len(self.rules)} heuristic rules")
        
    def _load_heuristic_rules(self) -> None:
        """Load heuristic detection rules"""
        # Initialize default rules
        default_rules = [
            HeuristicRule("HR001", "Suspicious API Usage", "behavioral", 0.8,
                         "Detects usage of APIs commonly used by malware"),
            HeuristicRule("HR002", "Code Injection Patterns", "behavioral", 0.9,
                         "Identifies potential code injection behavior"),
            HeuristicRule("HR003", "Anti-Analysis Techniques", "behavioral", 0.7,
                         "Detects anti-debugging and anti-VM techniques"),
            HeuristicRule("HR004", "Unusual File Structure", "structural", 0.6,
                         "Identifies anomalies in file structure"),
            HeuristicRule("HR005", "High Entropy Sections", "anomaly", 0.7,
                         "Detects potentially packed or encrypted sections"),
            HeuristicRule("HR006", "Suspicious String Patterns", "behavioral", 0.5,
                         "Identifies suspicious string patterns in binaries"),
        ]
        
        for rule in default_rules:
            self.rules[rule.rule_id] = rule
            
    def _load_suspicious_patterns(self) -> None:
        """Load patterns for suspicious APIs and strings"""
        # Common malicious APIs
        self.suspicious_apis = {
            'VirtualAllocEx', 'WriteProcessMemory', 'CreateRemoteThread',
            'SetWindowsHookEx', 'GetAsyncKeyState', 'GetKeyState',
            'CreateToolhelp32Snapshot', 'Process32First', 'Process32Next',
            'OpenProcess', 'ReadProcessMemory', 'NtUnmapViewOfSection',
            'RegSetValueEx', 'RegCreateKeyEx', 'InternetOpenUrl',
            'URLDownloadToFile', 'WinExec', 'ShellExecute',
            'IsDebuggerPresent', 'CheckRemoteDebuggerPresent',
            'FindWindow', 'GetForegroundWindow', 'GetWindowText'
        }
        
        # Suspicious strings
        self.suspicious_strings = {
            'cmd.exe', 'powershell.exe', 'wscript.exe', 'cscript.exe',
            'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run',
            'HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run',
            '\\System32\\', '\\SysWOW64\\', 'kernel32.dll', 'ntdll.dll',
            'password', 'passwd', 'credit_card', 'bitcoin', 'wallet',
            '.onion', 'tor2web', 'torproject', 'ransomware',
            'encrypt', 'decrypt', 'payment', 'bitcoin_address'
        }
        
    def scan_file(self, file_path: Path) -> ScanResult:
        """Scan a file using heuristic analysis"""
        if not self.is_initialized:
            raise HeuristicScannerError("Scanner not initialized")
            
        if not file_path.exists():
            raise HeuristicScannerError(f"File not found: {file_path}")
            
        logger.debug(f"Performing heuristic scan on: {file_path}")
        
        try:
            # Collect all heuristic indicators
            indicators = []
            threat_score = 0.0
            
            # Check file entropy
            entropy_result = self._check_file_entropy(file_path)
            if entropy_result:
                indicators.append(entropy_result)
                threat_score += entropy_result['weight']
                
            # Analyze PE structure (if applicable)
            if self._is_pe_file(file_path):
                pe_results = self._analyze_pe_structure(file_path)
                indicators.extend(pe_results)
                threat_score += sum(r['weight'] for r in pe_results)
                
            # Check for suspicious strings
            string_results = self._check_suspicious_strings(file_path)
            indicators.extend(string_results)
            threat_score += sum(r['weight'] for r in string_results)
            
            # Check for suspicious patterns
            pattern_results = self._check_behavioral_patterns(file_path)
            indicators.extend(pattern_results)
            threat_score += sum(r['weight'] for r in pattern_results)
            
            # Determine if threat detected based on cumulative score
            threat_detected = threat_score >= self.config.get('threat_threshold', 1.0)
            confidence = min(threat_score / self.config.get('max_score', 5.0), 1.0)
            
            # Classify threat type based on indicators
            threat_type = self._classify_threat(indicators) if threat_detected else None
            
            return ScanResult(
                file_path=str(file_path),
                threat_detected=threat_detected,
                threat_type=threat_type,
                confidence=confidence,
                details={
                    'scan_type': 'heuristic',
                    'threat_score': threat_score,
                    'indicators': indicators,
                    'rules_triggered': [ind['rule_id'] for ind in indicators]
                }
            )
            
        except Exception as e:
            logger.error(f"Error during heuristic scan of {file_path}: {str(e)}")
            raise HeuristicScannerError(f"Heuristic scan failed: {str(e)}")
            
    def scan_directory(self, directory_path: Path, recursive: bool = True) -> List[ScanResult]:
        """Scan a directory using heuristic analysis"""
        if not self.is_initialized:
            raise HeuristicScannerError("Scanner not initialized")
            
        if not directory_path.exists() or not directory_path.is_dir():
            raise HeuristicScannerError(f"Invalid directory: {directory_path}")
            
        results = []
        pattern = "**/*" if recursive else "*"
        
        for file_path in directory_path.glob(pattern):
            if file_path.is_file():
                try:
                    result = self.scan_file(file_path)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Failed to scan {file_path}: {str(e)}")
                    
        return results
        
    def update_definitions(self) -> bool:
        """Update heuristic rules and patterns"""
        try:
            # TODO: Implement rule update mechanism
            logger.info("Updating heuristic rules and patterns...")
            # Placeholder for update logic
            return True
        except Exception as e:
            logger.error(f"Failed to update heuristic definitions: {str(e)}")
            return False
            
    def _check_file_entropy(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Calculate and check file entropy for potential packing/encryption"""
        try:
            entropy = self._calculate_entropy(file_path)
            
            if entropy >= self.file_anomaly_thresholds['entropy_threshold']:
                return {
                    'rule_id': 'HR005',
                    'indicator': 'High file entropy',
                    'value': entropy,
                    'weight': self.rules['HR005'].weight,
                    'severity': 'medium'
                }
        except Exception as e:
            logger.error(f"Error calculating entropy: {str(e)}")
            
        return None
        
    def _calculate_entropy(self, file_path: Path) -> float:
        """Calculate Shannon entropy of a file"""
        with open(file_path, 'rb') as f:
            data = f.read()
            
        if not data:
            return 0.0
            
        # Calculate byte frequency
        frequency = {}
        for byte in data:
            frequency[byte] = frequency.get(byte, 0) + 1
            
        # Calculate entropy
        entropy = 0.0
        data_len = len(data)
        
        for count in frequency.values():
            if count > 0:
                probability = count / data_len
                entropy -= probability * (probability.bit_length() - 1)
                
        return entropy
        
    def _is_pe_file(self, file_path: Path) -> bool:
        """Check if file is a PE (Portable Executable) file"""
        try:
            with open(file_path, 'rb') as f:
                # Check DOS header magic number
                dos_header = f.read(2)
                return dos_header == b'MZ'
        except:
            return False
            
    def _analyze_pe_structure(self, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze PE file structure for anomalies"""
        indicators = []
        
        # TODO: Implement detailed PE analysis
        # This is a placeholder for PE structure analysis
        
        return indicators
        
    def _check_suspicious_strings(self, file_path: Path) -> List[Dict[str, Any]]:
        """Check for suspicious strings in the file"""
        indicators = []
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                
            # Extract printable strings
            strings = self._extract_strings(content)
            
            # Check against suspicious patterns
            for string in strings:
                for suspicious in self.suspicious_strings:
                    if suspicious.lower() in string.lower():
                        indicators.append({
                            'rule_id': 'HR006',
                            'indicator': f'Suspicious string found',
                            'value': string[:50],  # Truncate for display
                            'weight': self.rules['HR006'].weight,
                            'severity': 'low'
                        })
                        break
                        
        except Exception as e:
            logger.error(f"Error checking strings: {str(e)}")
            
        return indicators
        
    def _extract_strings(self, data: bytes, min_length: int = 4) -> List[str]:
        """Extract printable strings from binary data"""
        # Simple ASCII string extraction
        pattern = rb'[\x20-\x7E]{%d,}' % min_length
        strings = re.findall(pattern, data)
        return [s.decode('ascii', errors='ignore') for s in strings]
        
    def _check_behavioral_patterns(self, file_path: Path) -> List[Dict[str, Any]]:
        """Check for suspicious behavioral patterns"""
        indicators = []
        
        # TODO: Implement behavioral pattern detection
        # This would include checking for:
        # - API import analysis
        # - Code pattern analysis
        # - Anti-analysis techniques
        
        return indicators
        
    def _classify_threat(self, indicators: List[Dict[str, Any]]) -> str:
        """Classify the type of threat based on indicators"""
        # Simple classification based on indicator patterns
        categories = {}
        
        for indicator in indicators:
            rule = self.rules.get(indicator['rule_id'])
            if rule:
                category = rule.category
                categories[category] = categories.get(category, 0) + 1
                
        # Return the most common category
        if categories:
            return max(categories, key=categories.get)
            
        return "Unknown"
        
    def add_rule(self, rule: HeuristicRule) -> None:
        """Add a new heuristic rule"""
        self.rules[rule.rule_id] = rule
        logger.debug(f"Added heuristic rule: {rule.name}")
        
    def disable_rule(self, rule_id: str) -> bool:
        """Disable a heuristic rule"""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = False
            logger.debug(f"Disabled rule: {rule_id}")
            return True
        return False
        
    def get_rule_statistics(self) -> Dict[str, Any]:
        """Get statistics about heuristic rules"""
        return {
            'total_rules': len(self.rules),
            'enabled_rules': sum(1 for r in self.rules.values() if r.enabled),
            'categories': {
                'behavioral': sum(1 for r in self.rules.values() if r.category == 'behavioral'),
                'structural': sum(1 for r in self.rules.values() if r.category == 'structural'),
                'anomaly': sum(1 for r in self.rules.values() if r.category == 'anomaly')
            }
        }
