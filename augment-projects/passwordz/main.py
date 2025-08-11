"""
Main entry point for the password extraction tool.
"""
import sys
import os
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from gui import MainWindow
from utils import logger

def main():
    """Main entry point for the application."""
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationName("Passwordz")
    app.setOrganizationName("Passwordz")
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        raise
