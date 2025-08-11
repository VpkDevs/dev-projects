"""
Statistics tracking for password extraction operations.
"""
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from utils import logger

@dataclass
class ExtractionSession:
    """Data class for tracking an extraction session."""
    timestamp: str
    profiles_scanned: int
    passwords_found: int
    unique_passwords: int
    browsers_used: List[str]
    duration_seconds: float
    errors_encountered: int
    success_rate: float

class StatisticsManager:
    """Manager for tracking and analyzing extraction statistics."""
    
    def __init__(self, stats_file: str = 'statistics.json'):
        """Initialize the statistics manager."""
        self.stats_file = stats_file
        self.current_session = None
        self.stats = self.load_statistics()
    
    def load_statistics(self) -> Dict[str, Any]:
        """Load statistics from file."""
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'sessions': [],
                'totals': {
                    'total_extractions': 0,
                    'total_passwords_found': 0,
                    'total_profiles_scanned': 0,
                    'total_time_spent': 0.0,
                    'average_passwords_per_session': 0.0,
                    'most_productive_browser': '',
                    'last_extraction': ''
                },
                'browser_stats': {},
                'daily_stats': {}
            }
    
    def save_statistics(self) -> bool:
        """Save statistics to file."""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=4, default=str)
            return True
        except Exception as e:
            logger.error(f"Error saving statistics: {e}")
            return False
    
    def start_session(self) -> None:
        """Start a new extraction session."""
        self.current_session = {
            'start_time': time.time(),
            'timestamp': datetime.now().isoformat(),
            'profiles_scanned': 0,
            'passwords_found': 0,
            'unique_passwords': 0,
            'browsers_used': set(),
            'errors_encountered': 0
        }
    
    def add_profile_result(self, browser_name: str, passwords_count: int, had_error: bool = False) -> None:
        """Add results from a profile extraction."""
        if not self.current_session:
            return
        
        self.current_session['profiles_scanned'] += 1
        self.current_session['passwords_found'] += passwords_count
        self.current_session['browsers_used'].add(browser_name)
        
        if had_error:
            self.current_session['errors_encountered'] += 1
        
        # Update browser-specific stats
        if browser_name not in self.stats['browser_stats']:
            self.stats['browser_stats'][browser_name] = {
                'total_extractions': 0,
                'total_passwords': 0,
                'total_profiles': 0,
                'success_rate': 0.0,
                'last_used': ''
            }
        
        browser_stats = self.stats['browser_stats'][browser_name]
        browser_stats['total_extractions'] += 1
        browser_stats['total_passwords'] += passwords_count
        browser_stats['total_profiles'] += 1
        browser_stats['last_used'] = datetime.now().isoformat()
        
        # Calculate success rate
        if browser_stats['total_extractions'] > 0:
            successful_extractions = browser_stats['total_extractions'] - (1 if had_error else 0)
            browser_stats['success_rate'] = (successful_extractions / browser_stats['total_extractions']) * 100
    
    def end_session(self, unique_passwords_count: int) -> ExtractionSession:
        """End the current session and save statistics."""
        if not self.current_session:
            return None
        
        # Calculate session duration
        duration = time.time() - self.current_session['start_time']
        
        # Calculate success rate
        total_operations = self.current_session['profiles_scanned']
        successful_operations = total_operations - self.current_session['errors_encountered']
        success_rate = (successful_operations / total_operations * 100) if total_operations > 0 else 0
        
        # Create session object
        session = ExtractionSession(
            timestamp=self.current_session['timestamp'],
            profiles_scanned=self.current_session['profiles_scanned'],
            passwords_found=self.current_session['passwords_found'],
            unique_passwords=unique_passwords_count,
            browsers_used=list(self.current_session['browsers_used']),
            duration_seconds=duration,
            errors_encountered=self.current_session['errors_encountered'],
            success_rate=success_rate
        )
        
        # Add to sessions list
        self.stats['sessions'].append(asdict(session))
        
        # Update totals
        totals = self.stats['totals']
        totals['total_extractions'] += 1
        totals['total_passwords_found'] += self.current_session['passwords_found']
        totals['total_profiles_scanned'] += self.current_session['profiles_scanned']
        totals['total_time_spent'] += duration
        totals['last_extraction'] = self.current_session['timestamp']
        
        # Calculate average passwords per session
        if totals['total_extractions'] > 0:
            totals['average_passwords_per_session'] = totals['total_passwords_found'] / totals['total_extractions']
        
        # Find most productive browser
        most_productive = max(
            self.stats['browser_stats'].items(),
            key=lambda x: x[1]['total_passwords'],
            default=('', {'total_passwords': 0})
        )
        totals['most_productive_browser'] = most_productive[0]
        
        # Update daily stats
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in self.stats['daily_stats']:
            self.stats['daily_stats'][today] = {
                'extractions': 0,
                'passwords_found': 0,
                'time_spent': 0.0
            }
        
        daily = self.stats['daily_stats'][today]
        daily['extractions'] += 1
        daily['passwords_found'] += self.current_session['passwords_found']
        daily['time_spent'] += duration
        
        # Save statistics
        self.save_statistics()
        
        # Clear current session
        self.current_session = None
        
        return session
    
    def get_recent_sessions(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get sessions from the last N days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_sessions = []
        
        for session in self.stats['sessions']:
            session_date = datetime.fromisoformat(session['timestamp'])
            if session_date >= cutoff_date:
                recent_sessions.append(session)
        
        return recent_sessions
    
    def get_browser_ranking(self) -> List[tuple]:
        """Get browsers ranked by total passwords found."""
        browser_stats = self.stats['browser_stats']
        return sorted(
            browser_stats.items(),
            key=lambda x: x[1]['total_passwords'],
            reverse=True
        )
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get a summary of all statistics."""
        totals = self.stats['totals']
        recent_sessions = self.get_recent_sessions(7)
        
        return {
            'total_extractions': totals['total_extractions'],
            'total_passwords_found': totals['total_passwords_found'],
            'total_profiles_scanned': totals['total_profiles_scanned'],
            'average_passwords_per_session': round(totals['average_passwords_per_session'], 2),
            'total_time_spent_hours': round(totals['total_time_spent'] / 3600, 2),
            'most_productive_browser': totals['most_productive_browser'],
            'last_extraction': totals['last_extraction'],
            'recent_sessions_count': len(recent_sessions),
            'recent_passwords_found': sum(s['passwords_found'] for s in recent_sessions),
            'browser_count': len(self.stats['browser_stats']),
            'average_session_duration': round(
                sum(s['duration_seconds'] for s in self.stats['sessions']) / len(self.stats['sessions'])
                if self.stats['sessions'] else 0, 2
            )
        }
    
    def export_statistics(self, file_path: str) -> bool:
        """Export statistics to a file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=4, default=str)
            return True
        except Exception as e:
            logger.error(f"Error exporting statistics: {e}")
            return False
    
    def clear_statistics(self) -> bool:
        """Clear all statistics."""
        try:
            self.stats = {
                'sessions': [],
                'totals': {
                    'total_extractions': 0,
                    'total_passwords_found': 0,
                    'total_profiles_scanned': 0,
                    'total_time_spent': 0.0,
                    'average_passwords_per_session': 0.0,
                    'most_productive_browser': '',
                    'last_extraction': ''
                },
                'browser_stats': {},
                'daily_stats': {}
            }
            return self.save_statistics()
        except Exception as e:
            logger.error(f"Error clearing statistics: {e}")
            return False
