"""
Password extractor module to extract passwords from browser profiles.
"""
import os
import json
import sqlite3
import shutil
import base64
import win32crypt
import tempfile
from typing import List, Dict, Any, Optional, Set
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from browser_detector import BrowserProfile
from utils import logger, is_process_running

class PasswordExtractor:
    """Class to extract passwords from browser profiles."""

    def __init__(self):
        """Initialize the password extractor."""
        self.temp_dir = tempfile.mkdtemp(prefix="passwordz_")

    def __del__(self):
        """Clean up temporary files."""
        try:
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            logger.error(f"Error cleaning up temp directory: {e}")

    def extract_passwords_from_profile(self, profile: BrowserProfile) -> List[str]:
        """Extract passwords from a browser profile."""
        if 'Firefox' in profile.browser_name:
            return self._extract_firefox_passwords(profile)
        else:
            return self._extract_chrome_based_passwords(profile)

    def _extract_chrome_based_passwords(self, profile: BrowserProfile) -> List[str]:
        """Extract passwords from Chrome-based browsers (Chrome, Edge, Brave)."""
        passwords = []

        # Check if browser is running
        browser_process_map = {
            'Google Chrome': 'chrome.exe',
            'Google Chrome Dev': 'chrome.exe',
            'Google Chrome Canary': 'chrome.exe',
            'Microsoft Edge': 'msedge.exe',
            'Microsoft Edge Canary': 'msedge.exe',
            'Microsoft Edge Dev': 'msedge.exe',
            'Brave Browser': 'brave.exe',
            'Opera': 'opera.exe',
            'Opera GX': 'opera.exe',
            'Opera One': 'opera.exe',
            'Vivaldi': 'vivaldi.exe',
            'Yandex Browser': 'browser.exe',
            'AVG Secure Browser': 'avg_browser.exe',
            'CCleaner Browser': 'ccleaner_browser.exe',
            'Naver Whale': 'whale.exe'
        }

        browser_process = browser_process_map.get(profile.browser_name)
        if browser_process and is_process_running(browser_process):
            logger.warning(f"{profile.browser_name} is running. Some passwords may not be accessible.")

        # Path to the Login Data file
        login_data_path = os.path.join(profile.profile_path, 'Login Data')
        if not os.path.exists(login_data_path):
            logger.warning(f"Login Data file not found for {profile}")
            return passwords

        # Copy the database to a temporary location (as it might be locked by the browser)
        temp_login_data = os.path.join(self.temp_dir, f"{profile.browser_name.replace(' ', '_')}_{profile.profile_name}_Login_Data")
        try:
            shutil.copy2(login_data_path, temp_login_data)

            # Connect to the database
            conn = sqlite3.connect(temp_login_data)
            cursor = conn.cursor()

            # Get the encryption key
            encryption_key = self._get_chrome_encryption_key(profile)
            if not encryption_key:
                logger.error(f"Could not get encryption key for {profile}")
                return passwords

            # Query for passwords with additional validation
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins WHERE password_value IS NOT NULL AND password_value != ''")
            for row in cursor.fetchall():
                origin_url, username, encrypted_password = row

                # Skip empty passwords
                if not encrypted_password:
                    continue

                # Decrypt the password
                decrypted_password = self._decrypt_chrome_password(encrypted_password, encryption_key)
                if decrypted_password and len(decrypted_password.strip()) > 0:
                    passwords.append(decrypted_password.strip())

            # Close the connection
            cursor.close()
            conn.close()

        except Exception as e:
            logger.error(f"Error extracting passwords from {profile}: {e}")
        finally:
            # Clean up
            try:
                os.remove(temp_login_data)
            except:
                pass

        return passwords

    def _extract_firefox_passwords(self, profile: BrowserProfile) -> List[str]:
        """Extract passwords from Firefox profiles."""
        passwords = []

        # Check if Firefox is running
        if is_process_running('firefox.exe'):
            logger.warning("Firefox is running. Some passwords may not be accessible.")

        # Path to the logins.json file
        logins_path = os.path.join(profile.profile_path, 'logins.json')
        if not os.path.exists(logins_path):
            logger.warning(f"logins.json file not found for {profile}")
            return passwords

        try:
            # Firefox uses a different encryption mechanism (NSS)
            # This is a simplified implementation and may not work for all Firefox profiles
            # A more complete solution would use the NSS library
            logger.warning("Firefox password extraction is limited and may not work for all profiles")

            with open(logins_path, 'r', encoding='utf-8') as f:
                logins_data = json.load(f)

                if 'logins' in logins_data:
                    for login in logins_data['logins']:
                        if 'encryptedPassword' in login:
                            # We can't fully decrypt Firefox passwords without NSS
                            # This is a placeholder for a more complete implementation
                            logger.info(f"Found encrypted Firefox password for {login.get('hostname', 'unknown site')}")

        except Exception as e:
            logger.error(f"Error extracting passwords from Firefox profile {profile}: {e}")

        return passwords

    def _get_chrome_encryption_key(self, profile: BrowserProfile) -> Optional[bytes]:
        """Get the encryption key for Chrome-based browsers."""
        try:
            # Path to the Local State file which contains the encrypted key
            local_state_path = os.path.join(os.path.dirname(profile.profile_path), 'Local State')

            with open(local_state_path, 'r', encoding='utf-8') as f:
                local_state = json.load(f)

            # Get the encrypted key
            encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])

            # Remove 'DPAPI' prefix
            encrypted_key = encrypted_key[5:]

            # Decrypt the key using Windows DPAPI
            decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

            return decrypted_key

        except Exception as e:
            logger.error(f"Error getting encryption key for {profile}: {e}")
            return None

    def _decrypt_chrome_password(self, encrypted_password: bytes, encryption_key: bytes) -> Optional[str]:
        """Decrypt a Chrome password using the encryption key."""
        try:
            # Check if password is encrypted with DPAPI
            if encrypted_password[:3] == b'v10' or encrypted_password[:3] == b'v11':
                # Get initialization vector
                iv = encrypted_password[3:15]
                encrypted_password = encrypted_password[15:]

                # Create cipher
                cipher = AESGCM(encryption_key)

                # Decrypt
                decrypted_password = cipher.decrypt(iv, encrypted_password, None)
                return decrypted_password.decode('utf-8')
            else:
                # Older versions use DPAPI directly
                decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]
                return decrypted_password.decode('utf-8')

        except Exception as e:
            logger.error(f"Error decrypting password: {e}")
            return None

    def extract_all_passwords(self, profiles: List[BrowserProfile]) -> List[str]:
        """Extract passwords from all profiles and return a unique, sorted list."""
        all_passwords: Set[str] = set()

        for profile in profiles:
            try:
                logger.info(f"Extracting passwords from {profile}")
                passwords = self.extract_passwords_from_profile(profile)
                all_passwords.update(passwords)
            except Exception as e:
                logger.error(f"Error processing profile {profile}: {e}")

        # Sort alphabetically
        return sorted(list(all_passwords))
