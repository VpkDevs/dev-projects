"""
Browser detection module to identify installed browsers and their profiles.
"""
import os
import json
import logging
import win32api
import win32con
from typing import List, Dict, Any, Optional, Tuple
from utils import get_app_data_path, get_user_home_path, get_windows_users, logger

class BrowserProfile:
    """Class representing a browser profile with its path and metadata."""

    def __init__(self, browser_name: str, profile_name: str, profile_path: str, user: str):
        self.browser_name = browser_name
        self.profile_name = profile_name
        self.profile_path = profile_path
        self.user = user

    def __str__(self) -> str:
        return f"{self.browser_name} - {self.profile_name} ({self.user})"

    def to_dict(self) -> Dict[str, str]:
        """Convert profile to dictionary for serialization."""
        return {
            'browser_name': self.browser_name,
            'profile_name': self.profile_name,
            'profile_path': self.profile_path,
            'user': self.user
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'BrowserProfile':
        """Create profile from dictionary."""
        return cls(
            data['browser_name'],
            data['profile_name'],
            data['profile_path'],
            data['user']
        )

class BrowserDetector:
    """Class to detect browsers and their profiles on the system."""

    def __init__(self):
        """Initialize the browser detector."""
        self.browsers = {
            'chrome': {
                'name': 'Google Chrome',
                'paths': [
                    os.path.join(get_app_data_path(), 'Google', 'Chrome', 'User Data'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            },
            'chrome_dev': {
                'name': 'Google Chrome Dev',
                'paths': [
                    os.path.join(get_app_data_path(), 'Google', 'Chrome Dev', 'User Data'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            },
            'chrome_canary': {
                'name': 'Google Chrome Canary',
                'paths': [
                    os.path.join(get_app_data_path(), 'Google', 'Chrome SxS', 'User Data'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            },
            'edge': {
                'name': 'Microsoft Edge',
                'paths': [
                    os.path.join(get_app_data_path(), 'Microsoft', 'Edge', 'User Data'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            },
            'edge_canary': {
                'name': 'Microsoft Edge Canary',
                'paths': [
                    os.path.join(get_app_data_path(), 'Microsoft', 'Edge Canary', 'User Data'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            },
            'edge_dev': {
                'name': 'Microsoft Edge Dev',
                'paths': [
                    os.path.join(get_app_data_path(), 'Microsoft', 'Edge Dev', 'User Data'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            },
            'brave': {
                'name': 'Brave Browser',
                'paths': [
                    os.path.join(get_app_data_path(), 'BraveSoftware', 'Brave-Browser', 'User Data'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            },
            'firefox': {
                'name': 'Mozilla Firefox',
                'paths': [
                    os.path.join(get_app_data_path(), 'Mozilla', 'Firefox', 'Profiles'),
                    os.path.join(get_user_home_path(), 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
                ],
                'profile_pattern': '*.default*',
                'default_profile': None,
                'login_data_path': 'logins.json'
            },
            'opera': {
                'name': 'Opera',
                'paths': [
                    os.path.join(get_app_data_path(), 'Opera Software', 'Opera Stable'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            },
            'opera_gx': {
                'name': 'Opera GX',
                'paths': [
                    os.path.join(get_app_data_path(), 'Opera Software', 'Opera GX Stable'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            },
            'opera_one': {
                'name': 'Opera One',
                'paths': [
                    os.path.join(get_app_data_path(), 'Opera Software', 'Opera One Stable'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            },
            'vivaldi': {
                'name': 'Vivaldi',
                'paths': [
                    os.path.join(get_app_data_path(), 'Vivaldi', 'User Data'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            },
            'yandex': {
                'name': 'Yandex Browser',
                'paths': [
                    os.path.join(get_app_data_path(), 'Yandex', 'YandexBrowser', 'User Data'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            },
            'avg': {
                'name': 'AVG Secure Browser',
                'paths': [
                    os.path.join(get_app_data_path(), 'AVG', 'Browser', 'User Data'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            },
            'ccleaner': {
                'name': 'CCleaner Browser',
                'paths': [
                    os.path.join(get_app_data_path(), 'CCleaner', 'CCleaner Browser', 'User Data'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            },
            'whale': {
                'name': 'Naver Whale',
                'paths': [
                    os.path.join(get_app_data_path(), 'Naver', 'Naver Whale', 'User Data'),
                ],
                'profile_pattern': 'Profile *',
                'default_profile': 'Default',
                'login_data_path': 'Login Data'
            }
        }

    def detect_all_profiles(self) -> List[BrowserProfile]:
        """Detect all browser profiles on the system for all users."""
        all_profiles = []

        # Get all Windows users
        windows_users = get_windows_users()
        current_user = os.environ.get('USERNAME')

        # First check current user
        if current_user in windows_users:
            profiles = self._detect_profiles_for_user(current_user)
            all_profiles.extend(profiles)
            windows_users.remove(current_user)

        # Then check other users
        for user in windows_users:
            profiles = self._detect_profiles_for_user(user)
            all_profiles.extend(profiles)

        return all_profiles

    def _detect_profiles_for_user(self, username: str) -> List[BrowserProfile]:
        """Detect browser profiles for a specific Windows user."""
        profiles = []

        # Construct the user's AppData path
        user_path = os.path.join(os.environ.get('SystemDrive', 'C:'), 'Users', username)
        if not os.path.exists(user_path):
            return []

        user_app_data = os.path.join(user_path, 'AppData', 'Local')
        user_roaming_app_data = os.path.join(user_path, 'AppData', 'Roaming')

        # Check each browser
        for browser_id, browser_info in self.browsers.items():
            for base_path in browser_info['paths']:
                # Replace the AppData path with the user-specific one
                if 'AppData\\Local' in base_path:
                    browser_path = base_path.replace(get_app_data_path(), user_app_data)
                elif 'AppData\\Roaming' in base_path:
                    browser_path = base_path.replace(
                        os.path.join(get_user_home_path(), 'AppData', 'Roaming'),
                        user_roaming_app_data
                    )
                else:
                    continue

                if not os.path.exists(browser_path):
                    continue

                # Handle different profile structures for different browsers
                if browser_id == 'firefox':
                    # Firefox has a different profile structure
                    try:
                        for profile_dir in os.listdir(browser_path):
                            if profile_dir.endswith('.default') or profile_dir.endswith('.default-release'):
                                profile_path = os.path.join(browser_path, profile_dir)
                                profile = BrowserProfile(
                                    browser_info['name'],
                                    profile_dir,
                                    profile_path,
                                    username
                                )
                                profiles.append(profile)
                    except Exception as e:
                        logger.error(f"Error detecting Firefox profiles for user {username}: {e}")
                else:
                    # Chrome, Edge, Brave have similar profile structures
                    try:
                        # Check default profile
                        default_profile_path = os.path.join(browser_path, browser_info['default_profile'])
                        if os.path.exists(default_profile_path):
                            profile = BrowserProfile(
                                browser_info['name'],
                                'Default',
                                default_profile_path,
                                username
                            )
                            profiles.append(profile)

                        # Check numbered profiles
                        for i in range(1, 100):  # Check up to 100 profiles
                            profile_dir = f"Profile {i}"
                            profile_path = os.path.join(browser_path, profile_dir)
                            if os.path.exists(profile_path):
                                # Try to get the profile name from the Preferences file
                                profile_name = self._get_chrome_profile_name(profile_path, profile_dir)
                                profile = BrowserProfile(
                                    browser_info['name'],
                                    profile_name,
                                    profile_path,
                                    username
                                )
                                profiles.append(profile)
                    except Exception as e:
                        logger.error(f"Error detecting {browser_info['name']} profiles for user {username}: {e}")

        return profiles

    def _get_chrome_profile_name(self, profile_path: str, default_name: str) -> str:
        """Get the profile name from Chrome/Edge/Brave Preferences file."""
        try:
            prefs_path = os.path.join(profile_path, 'Preferences')
            if os.path.exists(prefs_path):
                with open(prefs_path, 'r', encoding='utf-8') as f:
                    prefs = json.load(f)
                    if 'profile' in prefs and 'name' in prefs['profile']:
                        return prefs['profile']['name']
        except Exception as e:
            logger.error(f"Error reading profile name from {profile_path}: {e}")

        return default_name
