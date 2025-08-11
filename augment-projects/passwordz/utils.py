"""
Utility functions for the password extraction tool.
"""
import os
import logging
import platform
import subprocess
from typing import List, Dict, Any, Optional
import yaml

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("passwordz.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("passwordz")

def get_app_data_path() -> str:
    """Get the path to the AppData directory."""
    return os.path.join(os.environ['LOCALAPPDATA'])

def get_user_home_path() -> str:
    """Get the path to the user's home directory."""
    return os.path.expanduser('~')

def get_windows_users() -> List[str]:
    """Get a list of all Windows user accounts on the system."""
    try:
        # For simplicity, just return the current user
        current_user = os.environ.get('USERNAME')
        if current_user:
            return [current_user]
        else:
            return []
    except Exception as e:
        logger.error(f"Error getting Windows users: {e}")
        return []

def is_process_running(process_name: str) -> bool:
    """Check if a process is running by name."""
    try:
        output = subprocess.check_output(['tasklist', '/FI', f'IMAGENAME eq {process_name}'],
                                        text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return process_name.lower() in output.lower()
    except Exception as e:
        logger.error(f"Error checking if process {process_name} is running: {e}")
        return False

def save_config(config: Dict[str, Any], filename: str = 'config.yaml') -> bool:
    """Save configuration to a YAML file."""
    try:
        with open(filename, 'w') as f:
            yaml.dump(config, f)
        return True
    except Exception as e:
        logger.error(f"Error saving config: {e}")
        return False

def load_config(filename: str = 'config.yaml') -> Optional[Dict[str, Any]]:
    """Load configuration from a YAML file."""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Error loading config: {e}")
    return None

def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename
