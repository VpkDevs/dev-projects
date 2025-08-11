"""
Base Scanner Module
Provides abstract base class for all scanner implementations
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class BaseScannerError(Exception):
    """Base exception for scanner errors"""
    pass


class ScanResult:
    """Represents the result of a scan operation"""
    
    def __init__(self, file_path: str, threat_detected: bool = False, 
                 threat_type: Optional[str] = None, confidence: float = 0.0,
                 details: Optional[Dict[str, Any]] = None):
        self.file_path = file_path
        self.threat_detected = threat_detected
        self.threat_type = threat_type
        self.confidence = confidence
        self.details = details or {}
        self.timestamp = None  # Will be set by scanner
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert scan result to dictionary format"""
        return {
            'file_path': self.file_path,
            'threat_detected': self.threat_detected,
            'threat_type': self.threat_type,
            'confidence': self.confidence,
            'details': self.details,
            'timestamp': self.timestamp
        }


class BaseScanner(ABC):
    """Abstract base class for all scanner implementations"""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.is_initialized = False
        
    def initialize(self) -> None:
        """Initialize the scanner with necessary resources"""
        logger.info(f"Initializing {self.name} scanner")
        self._initialize()
        self.is_initialized = True
        
    @abstractmethod
    def _initialize(self) -> None:
        """Scanner-specific initialization logic"""
        pass
        
    @abstractmethod
    def scan_file(self, file_path: Path) -> ScanResult:
        """Scan a single file for threats"""
        pass
        
    @abstractmethod
    def scan_directory(self, directory_path: Path, recursive: bool = True) -> List[ScanResult]:
        """Scan a directory for threats"""
        pass
        
    @abstractmethod
    def update_definitions(self) -> bool:
        """Update scanner definitions/rules"""
        pass
        
    def cleanup(self) -> None:
        """Cleanup scanner resources"""
        logger.info(f"Cleaning up {self.name} scanner")
        self._cleanup()
        self.is_initialized = False
        
    def _cleanup(self) -> None:
        """Scanner-specific cleanup logic"""
        pass
        
    def get_scanner_info(self) -> Dict[str, Any]:
        """Get information about the scanner"""
        return {
            'name': self.name,
            'type': self.__class__.__name__,
            'is_initialized': self.is_initialized,
            'config': self.config
        }
