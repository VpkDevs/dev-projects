"""
Configuration management for the password extraction tool.
"""
import os
import json
from typing import Dict, Any, Optional
from utils import logger

class Config:
    """Configuration manager for the application."""
    
    def __init__(self, config_file: str = 'config.json'):
        """Initialize the configuration manager."""
        self.config_file = config_file
        self.default_config = {
            'ui': {
                'window_width': 1000,
                'window_height': 700,
                'splitter_sizes': [250, 350, 100],
                'remember_window_size': True,
                'theme': 'default'
            },
            'extraction': {
                'auto_detect_profiles': True,
                'include_empty_passwords': False,
                'max_password_length': 1000,
                'timeout_seconds': 30,
                'retry_attempts': 3
            },
            'security': {
                'auto_encrypt_saves': True,
                'clear_clipboard_after': 60,
                'log_level': 'INFO',
                'secure_delete_temp_files': True
            },
            'browsers': {
                'enabled_browsers': [
                    'chrome', 'chrome_dev', 'chrome_canary',
                    'edge', 'edge_canary', 'edge_dev',
                    'brave', 'firefox', 'opera', 'opera_gx', 'opera_one',
                    'vivaldi', 'yandex', 'avg', 'ccleaner', 'whale'
                ],
                'check_running_processes': True,
                'force_close_browsers': False
            },
            'export': {
                'default_format': 'txt',
                'include_metadata': False,
                'sort_alphabetically': True,
                'remove_duplicates': True
            }
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return self._merge_configs(self.default_config, loaded_config)
            else:
                # Create default config file
                self.save_config(self.default_config)
                return self.default_config.copy()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self.default_config.copy()
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Save configuration to file."""
        try:
            config_to_save = config or self.config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False
    
    def get(self, key_path: str, default=None):
        """Get a configuration value using dot notation (e.g., 'ui.window_width')."""
        try:
            keys = key_path.split('.')
            value = self.config
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> bool:
        """Set a configuration value using dot notation."""
        try:
            keys = key_path.split('.')
            config_ref = self.config
            for key in keys[:-1]:
                if key not in config_ref:
                    config_ref[key] = {}
                config_ref = config_ref[key]
            config_ref[keys[-1]] = value
            return True
        except Exception as e:
            logger.error(f"Error setting config value {key_path}: {e}")
            return False
    
    def _merge_configs(self, default: Dict[str, Any], loaded: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge loaded config with default config."""
        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to default values."""
        try:
            self.config = self.default_config.copy()
            return self.save_config()
        except Exception as e:
            logger.error(f"Error resetting config: {e}")
            return False
    
    def export_config(self, file_path: str) -> bool:
        """Export current configuration to a file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Error exporting config: {e}")
            return False
    
    def import_config(self, file_path: str) -> bool:
        """Import configuration from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
                self.config = self._merge_configs(self.default_config, imported_config)
                return self.save_config()
        except Exception as e:
            logger.error(f"Error importing config: {e}")
            return False
