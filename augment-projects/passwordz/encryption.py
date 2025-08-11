"""
Encryption and decryption utilities for secure password handling.
"""
import os
import base64
import logging
from typing import Optional, Tuple, List
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.fernet import Fernet

from utils import logger

class PasswordEncryption:
    """Class to handle encryption and decryption of password data."""
    
    def __init__(self, key_file: str = 'encryption.key'):
        """Initialize the encryption handler with a key file."""
        self.key_file = key_file
        self.key = self._load_or_generate_key()
        
    def _load_or_generate_key(self) -> bytes:
        """Load an existing key or generate a new one if it doesn't exist."""
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, 'rb') as f:
                    return base64.urlsafe_b64decode(f.read())
            else:
                # Generate a new key
                key = Fernet.generate_key()
                with open(self.key_file, 'wb') as f:
                    f.write(base64.urlsafe_b64encode(key))
                return base64.urlsafe_b64decode(key)
        except Exception as e:
            logger.error(f"Error with encryption key: {e}")
            # Generate a temporary key if there's an error
            return Fernet.generate_key()
    
    def encrypt_password_list(self, passwords: List[str]) -> bytes:
        """Encrypt a list of passwords."""
        try:
            # Convert list to a single string with newlines
            data = '\n'.join(passwords).encode('utf-8')
            
            # Generate a random 96-bit IV
            iv = os.urandom(12)
            
            # Create an AESGCM cipher with our key
            cipher = AESGCM(self.key)
            
            # Encrypt the data
            encrypted_data = cipher.encrypt(iv, data, None)
            
            # Return IV + encrypted data
            return base64.urlsafe_b64encode(iv + encrypted_data)
        except Exception as e:
            logger.error(f"Error encrypting passwords: {e}")
            return b''
    
    def decrypt_password_list(self, encrypted_data: bytes) -> List[str]:
        """Decrypt a list of passwords."""
        try:
            # Decode from base64
            data = base64.urlsafe_b64decode(encrypted_data)
            
            # Extract IV (first 12 bytes) and ciphertext
            iv = data[:12]
            ciphertext = data[12:]
            
            # Create an AESGCM cipher with our key
            cipher = AESGCM(self.key)
            
            # Decrypt the data
            decrypted_data = cipher.decrypt(iv, ciphertext, None)
            
            # Convert back to a list of passwords
            return decrypted_data.decode('utf-8').split('\n')
        except Exception as e:
            logger.error(f"Error decrypting passwords: {e}")
            return []
    
    def encrypt_single_password(self, password: str) -> bytes:
        """Encrypt a single password."""
        return self.encrypt_password_list([password])
    
    def decrypt_single_password(self, encrypted_data: bytes) -> Optional[str]:
        """Decrypt a single password."""
        passwords = self.decrypt_password_list(encrypted_data)
        return passwords[0] if passwords else None
