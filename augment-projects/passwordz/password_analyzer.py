"""
Password strength analysis and security assessment tools.
"""
import re
import math
from typing import List, Dict, Any, Tuple
from collections import Counter
from dataclasses import dataclass

@dataclass
class PasswordAnalysis:
    """Data class for password analysis results."""
    password: str
    length: int
    strength_score: float
    strength_level: str
    has_uppercase: bool
    has_lowercase: bool
    has_digits: bool
    has_symbols: bool
    entropy: float
    common_patterns: List[str]
    estimated_crack_time: str
    recommendations: List[str]

class PasswordAnalyzer:
    """Analyzer for password strength and security assessment."""
    
    def __init__(self):
        """Initialize the password analyzer."""
        self.common_passwords = self._load_common_passwords()
        self.common_patterns = [
            r'123+',  # Sequential numbers
            r'abc+',  # Sequential letters
            r'qwerty',  # Keyboard patterns
            r'password',  # Common words
            r'admin',
            r'user',
            r'login',
            r'(\w)\1{2,}',  # Repeated characters
            r'\d{4}',  # Years/dates
        ]
    
    def _load_common_passwords(self) -> set:
        """Load a set of common passwords for checking."""
        # This is a simplified list - in production, you'd load from a file
        return {
            'password', '123456', 'password123', 'admin', 'qwerty',
            'letmein', 'welcome', 'monkey', '1234567890', 'abc123',
            'password1', 'qwerty123', 'welcome123', 'admin123',
            'user', 'guest', 'test', 'demo', 'root', 'toor'
        }
    
    def analyze_password(self, password: str) -> PasswordAnalysis:
        """Perform comprehensive analysis of a password."""
        if not password:
            return self._create_empty_analysis()
        
        # Basic character analysis
        length = len(password)
        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_lowercase = bool(re.search(r'[a-z]', password))
        has_digits = bool(re.search(r'\d', password))
        has_symbols = bool(re.search(r'[^A-Za-z0-9]', password))
        
        # Calculate entropy
        entropy = self._calculate_entropy(password)
        
        # Detect common patterns
        common_patterns = self._detect_patterns(password)
        
        # Calculate strength score
        strength_score = self._calculate_strength_score(
            password, length, has_uppercase, has_lowercase,
            has_digits, has_symbols, entropy, common_patterns
        )
        
        # Determine strength level
        strength_level = self._get_strength_level(strength_score)
        
        # Estimate crack time
        crack_time = self._estimate_crack_time(entropy, strength_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            password, length, has_uppercase, has_lowercase,
            has_digits, has_symbols, common_patterns
        )
        
        return PasswordAnalysis(
            password=password,
            length=length,
            strength_score=strength_score,
            strength_level=strength_level,
            has_uppercase=has_uppercase,
            has_lowercase=has_lowercase,
            has_digits=has_digits,
            has_symbols=has_symbols,
            entropy=entropy,
            common_patterns=common_patterns,
            estimated_crack_time=crack_time,
            recommendations=recommendations
        )
    
    def analyze_password_list(self, passwords: List[str]) -> Dict[str, Any]:
        """Analyze a list of passwords and provide aggregate statistics."""
        if not passwords:
            return self._create_empty_list_analysis()
        
        analyses = [self.analyze_password(pwd) for pwd in passwords]
        
        # Calculate aggregate statistics
        total_passwords = len(passwords)
        unique_passwords = len(set(passwords))
        
        # Strength distribution
        strength_distribution = Counter(analysis.strength_level for analysis in analyses)
        
        # Average metrics
        avg_length = sum(analysis.length for analysis in analyses) / total_passwords
        avg_entropy = sum(analysis.entropy for analysis in analyses) / total_passwords
        avg_strength = sum(analysis.strength_score for analysis in analyses) / total_passwords
        
        # Character type usage
        uppercase_usage = sum(1 for analysis in analyses if analysis.has_uppercase) / total_passwords * 100
        lowercase_usage = sum(1 for analysis in analyses if analysis.has_lowercase) / total_passwords * 100
        digits_usage = sum(1 for analysis in analyses if analysis.has_digits) / total_passwords * 100
        symbols_usage = sum(1 for analysis in analyses if analysis.has_symbols) / total_passwords * 100
        
        # Common passwords
        common_passwords_found = sum(1 for pwd in passwords if pwd.lower() in self.common_passwords)
        
        # Pattern analysis
        all_patterns = []
        for analysis in analyses:
            all_patterns.extend(analysis.common_patterns)
        pattern_frequency = Counter(all_patterns)
        
        # Length distribution
        length_distribution = Counter(analysis.length for analysis in analyses)
        
        return {
            'total_passwords': total_passwords,
            'unique_passwords': unique_passwords,
            'duplicate_rate': (total_passwords - unique_passwords) / total_passwords * 100,
            'strength_distribution': dict(strength_distribution),
            'average_length': round(avg_length, 2),
            'average_entropy': round(avg_entropy, 2),
            'average_strength_score': round(avg_strength, 2),
            'character_usage': {
                'uppercase': round(uppercase_usage, 2),
                'lowercase': round(lowercase_usage, 2),
                'digits': round(digits_usage, 2),
                'symbols': round(symbols_usage, 2)
            },
            'common_passwords_found': common_passwords_found,
            'common_passwords_rate': common_passwords_found / total_passwords * 100,
            'pattern_frequency': dict(pattern_frequency.most_common(10)),
            'length_distribution': dict(length_distribution),
            'security_recommendations': self._generate_list_recommendations(analyses)
        }
    
    def _calculate_entropy(self, password: str) -> float:
        """Calculate the entropy of a password."""
        if not password:
            return 0.0
        
        # Determine character set size
        charset_size = 0
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'\d', password):
            charset_size += 10
        if re.search(r'[^A-Za-z0-9]', password):
            charset_size += 32  # Approximate number of common symbols
        
        if charset_size == 0:
            return 0.0
        
        # Calculate entropy: log2(charset_size^length)
        entropy = len(password) * math.log2(charset_size)
        return entropy
    
    def _detect_patterns(self, password: str) -> List[str]:
        """Detect common patterns in a password."""
        detected_patterns = []
        
        for pattern in self.common_patterns:
            if re.search(pattern, password.lower()):
                detected_patterns.append(pattern)
        
        # Check if it's a common password
        if password.lower() in self.common_passwords:
            detected_patterns.append('common_password')
        
        return detected_patterns
    
    def _calculate_strength_score(self, password: str, length: int, has_uppercase: bool,
                                has_lowercase: bool, has_digits: bool, has_symbols: bool,
                                entropy: float, patterns: List[str]) -> float:
        """Calculate a strength score from 0 to 100."""
        score = 0.0
        
        # Length scoring (0-30 points)
        if length >= 12:
            score += 30
        elif length >= 8:
            score += 20
        elif length >= 6:
            score += 10
        
        # Character diversity (0-40 points)
        char_types = sum([has_uppercase, has_lowercase, has_digits, has_symbols])
        score += char_types * 10
        
        # Entropy bonus (0-20 points)
        if entropy >= 60:
            score += 20
        elif entropy >= 40:
            score += 15
        elif entropy >= 25:
            score += 10
        
        # Pattern penalties (0-30 points deduction)
        penalty = min(len(patterns) * 10, 30)
        score -= penalty
        
        # Common password penalty
        if 'common_password' in patterns:
            score -= 50
        
        return max(0, min(100, score))
    
    def _get_strength_level(self, score: float) -> str:
        """Convert strength score to a descriptive level."""
        if score >= 80:
            return 'Very Strong'
        elif score >= 60:
            return 'Strong'
        elif score >= 40:
            return 'Moderate'
        elif score >= 20:
            return 'Weak'
        else:
            return 'Very Weak'
    
    def _estimate_crack_time(self, entropy: float, strength_score: float) -> str:
        """Estimate time to crack the password."""
        if strength_score < 20:
            return 'Instantly'
        elif strength_score < 40:
            return 'Minutes to Hours'
        elif strength_score < 60:
            return 'Days to Weeks'
        elif strength_score < 80:
            return 'Months to Years'
        else:
            return 'Centuries'
    
    def _generate_recommendations(self, password: str, length: int, has_uppercase: bool,
                                has_lowercase: bool, has_digits: bool, has_symbols: bool,
                                patterns: List[str]) -> List[str]:
        """Generate recommendations for improving password strength."""
        recommendations = []
        
        if length < 8:
            recommendations.append('Increase length to at least 8 characters')
        elif length < 12:
            recommendations.append('Consider increasing length to 12+ characters for better security')
        
        if not has_uppercase:
            recommendations.append('Add uppercase letters')
        if not has_lowercase:
            recommendations.append('Add lowercase letters')
        if not has_digits:
            recommendations.append('Add numbers')
        if not has_symbols:
            recommendations.append('Add special characters')
        
        if 'common_password' in patterns:
            recommendations.append('Avoid using common passwords')
        
        if any(pattern in patterns for pattern in ['123+', 'abc+', 'qwerty']):
            recommendations.append('Avoid sequential or keyboard patterns')
        
        if '(\\w)\\1{2,}' in patterns:
            recommendations.append('Avoid repeating characters')
        
        return recommendations
    
    def _generate_list_recommendations(self, analyses: List[PasswordAnalysis]) -> List[str]:
        """Generate recommendations for the entire password list."""
        recommendations = []
        
        weak_passwords = sum(1 for analysis in analyses if analysis.strength_score < 40)
        if weak_passwords > 0:
            recommendations.append(f'Replace {weak_passwords} weak passwords')
        
        common_passwords = sum(1 for analysis in analyses if 'common_password' in analysis.common_patterns)
        if common_passwords > 0:
            recommendations.append(f'Replace {common_passwords} common passwords')
        
        short_passwords = sum(1 for analysis in analyses if analysis.length < 8)
        if short_passwords > 0:
            recommendations.append(f'Increase length of {short_passwords} short passwords')
        
        return recommendations
    
    def _create_empty_analysis(self) -> PasswordAnalysis:
        """Create an empty analysis for invalid passwords."""
        return PasswordAnalysis(
            password='',
            length=0,
            strength_score=0.0,
            strength_level='Invalid',
            has_uppercase=False,
            has_lowercase=False,
            has_digits=False,
            has_symbols=False,
            entropy=0.0,
            common_patterns=[],
            estimated_crack_time='N/A',
            recommendations=['Invalid password']
        )
    
    def _create_empty_list_analysis(self) -> Dict[str, Any]:
        """Create an empty analysis for empty password lists."""
        return {
            'total_passwords': 0,
            'unique_passwords': 0,
            'duplicate_rate': 0.0,
            'strength_distribution': {},
            'average_length': 0.0,
            'average_entropy': 0.0,
            'average_strength_score': 0.0,
            'character_usage': {
                'uppercase': 0.0,
                'lowercase': 0.0,
                'digits': 0.0,
                'symbols': 0.0
            },
            'common_passwords_found': 0,
            'common_passwords_rate': 0.0,
            'pattern_frequency': {},
            'length_distribution': {},
            'security_recommendations': ['No passwords to analyze']
        }
