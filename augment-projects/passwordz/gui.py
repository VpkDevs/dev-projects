"""
GUI module for the password extraction tool.
"""
import os
import sys
import time
import threading
from typing import List, Dict, Any, Optional, Callable
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QProgressBar, QMessageBox,
    QFileDialog, QCheckBox, QGroupBox, QListWidget, QListWidgetItem,
    QSplitter, QStatusBar, QComboBox
)
from PySide6.QtCore import Qt, Signal, Slot, QSize, QTimer, QEvent
from PySide6.QtGui import QIcon, QFont, QTextCursor

from browser_detector import BrowserProfile, BrowserDetector
from password_extractor import PasswordExtractor
from encryption import PasswordEncryption
from config import Config
from extraction_stats import StatisticsManager
from password_analyzer import PasswordAnalyzer
from utils import logger, save_config, load_config, sanitize_filename

class PasswordListWidget(QTextEdit):
    """Custom widget to display the password list."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setFont(QFont("Consolas", 10))
        self.setPlaceholderText("Extracted passwords will appear here...")

    def set_passwords(self, passwords: List[str]):
        """Set the password list to display."""
        self.clear()
        for password in passwords:
            self.append(password)

    def clear_passwords(self):
        """Clear the password list."""
        self.clear()

class ProfileListWidget(QListWidget):
    """Custom widget to display and select browser profiles."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QListWidget.ExtendedSelection)

    def set_profiles(self, profiles: List[BrowserProfile]):
        """Set the profile list to display."""
        self.clear()
        for profile in profiles:
            item = QListWidgetItem(f"{profile.browser_name} - {profile.profile_name} ({profile.user})")
            item.setData(Qt.UserRole, profile)
            self.addItem(item)

    def get_selected_profiles(self) -> List[BrowserProfile]:
        """Get the selected profiles."""
        selected_profiles = []
        for item in self.selectedItems():
            profile = item.data(Qt.UserRole)
            selected_profiles.append(profile)
        return selected_profiles

    def select_all(self):
        """Select all profiles."""
        for i in range(self.count()):
            self.item(i).setSelected(True)

    def deselect_all(self):
        """Deselect all profiles."""
        for i in range(self.count()):
            self.item(i).setSelected(False)

class LogWidget(QTextEdit):
    """Custom widget to display log messages."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setFont(QFont("Consolas", 9))
        self.setMaximumHeight(150)

    def append_log(self, message: str):
        """Append a log message."""
        self.append(message)
        self.moveCursor(QTextCursor.End)

class MainWindow(QMainWindow):
    """Main window for the password extraction tool."""

    # Signals for thread communication
    update_progress = Signal(int, str)
    extraction_complete = Signal(list)
    log_message = Signal(str)

    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("Passwordz - Password Extraction Tool")
        self.setMinimumSize(800, 600)

        # Initialize components
        self.config = Config()
        self.browser_detector = BrowserDetector()
        self.password_extractor = PasswordExtractor()
        self.encryption = PasswordEncryption()
        self.stats_manager = StatisticsManager()
        self.password_analyzer = PasswordAnalyzer()

        # Set up the UI
        self.setup_ui()

        # Apply configuration
        self.apply_config()

        # Detect browser profiles
        self.detect_profiles()

    def setup_ui(self):
        """Set up the user interface."""
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Create a splitter for resizable sections
        splitter = QSplitter(Qt.Vertical)

        # Top section: Profile selection and controls
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)

        # Profile selection group
        profile_group = QGroupBox("Browser Profiles")
        profile_layout = QVBoxLayout(profile_group)

        # Profile list
        self.profile_list = ProfileListWidget()
        profile_layout.addWidget(self.profile_list)

        # Profile selection buttons
        profile_buttons_layout = QHBoxLayout()
        self.select_all_button = QPushButton("Select All")
        self.select_all_button.clicked.connect(self.profile_list.select_all)
        self.deselect_all_button = QPushButton("Deselect All")
        self.deselect_all_button.clicked.connect(self.profile_list.deselect_all)
        self.refresh_button = QPushButton("Refresh Profiles")
        self.refresh_button.clicked.connect(self.detect_profiles)

        profile_buttons_layout.addWidget(self.select_all_button)
        profile_buttons_layout.addWidget(self.deselect_all_button)
        profile_buttons_layout.addWidget(self.refresh_button)
        profile_layout.addLayout(profile_buttons_layout)

        top_layout.addWidget(profile_group)

        # Action buttons
        actions_layout = QHBoxLayout()
        self.extract_button = QPushButton("Extract Passwords")
        self.extract_button.clicked.connect(self.extract_passwords)
        self.extract_button.setMinimumHeight(40)
        self.save_button = QPushButton("Save Passwords")
        self.save_button.clicked.connect(self.save_passwords)
        self.save_button.setEnabled(False)
        self.save_button.setMinimumHeight(40)
        self.analyze_button = QPushButton("Analyze Passwords")
        self.analyze_button.clicked.connect(self.analyze_passwords)
        self.analyze_button.setEnabled(False)
        self.analyze_button.setMinimumHeight(40)
        self.clear_button = QPushButton("Clear Results")
        self.clear_button.clicked.connect(self.clear_results)
        self.clear_button.setMinimumHeight(40)

        actions_layout.addWidget(self.extract_button)
        actions_layout.addWidget(self.save_button)
        actions_layout.addWidget(self.analyze_button)
        actions_layout.addWidget(self.clear_button)
        top_layout.addLayout(actions_layout)

        # Additional buttons row
        additional_actions_layout = QHBoxLayout()
        self.stats_button = QPushButton("View Statistics")
        self.stats_button.clicked.connect(self.show_statistics)
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.show_settings)

        additional_actions_layout.addWidget(self.stats_button)
        additional_actions_layout.addWidget(self.settings_button)
        additional_actions_layout.addStretch()  # Push buttons to the left
        top_layout.addLayout(additional_actions_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        top_layout.addWidget(self.progress_bar)

        # Middle section: Password list
        middle_widget = QWidget()
        middle_layout = QVBoxLayout(middle_widget)

        password_group = QGroupBox("Extracted Passwords")
        password_layout = QVBoxLayout(password_group)

        self.password_list = PasswordListWidget()
        password_layout.addWidget(self.password_list)

        middle_layout.addWidget(password_group)

        # Bottom section: Log
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)

        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)

        self.log_widget = LogWidget()
        log_layout.addWidget(self.log_widget)

        bottom_layout.addWidget(log_group)

        # Add widgets to splitter
        splitter.addWidget(top_widget)
        splitter.addWidget(middle_widget)
        splitter.addWidget(bottom_widget)

        # Set initial sizes
        splitter.setSizes([200, 300, 100])

        # Add splitter to main layout
        main_layout.addWidget(splitter)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Set the main widget
        self.setCentralWidget(main_widget)

        # Connect signals
        self.update_progress.connect(self.on_progress_update)
        self.extraction_complete.connect(self.on_extraction_complete)
        self.log_message.connect(self.on_log_message)

    def detect_profiles(self):
        """Detect browser profiles."""
        self.log_message.emit("Detecting browser profiles...")
        self.status_bar.showMessage("Detecting browser profiles...")

        # Run in a separate thread to avoid freezing the UI
        def detect_thread():
            try:
                profiles = self.browser_detector.detect_all_profiles()
                # Update UI in the main thread
                QApplication.instance().postEvent(
                    self,
                    UpdateProfilesEvent(profiles)
                )
            except Exception as e:
                logger.error(f"Error detecting profiles: {e}")
                self.log_message.emit(f"Error detecting profiles: {e}")

        threading.Thread(target=detect_thread).start()

    def extract_passwords(self):
        """Extract passwords from selected profiles."""
        selected_profiles = self.profile_list.get_selected_profiles()

        if not selected_profiles:
            QMessageBox.warning(
                self,
                "No Profiles Selected",
                "Please select at least one browser profile."
            )
            return

        # Disable buttons during extraction
        self.extract_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.analyze_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.refresh_button.setEnabled(False)

        # Clear previous results
        self.password_list.clear_passwords()
        self.progress_bar.setValue(0)

        self.log_message.emit(f"Starting password extraction from {len(selected_profiles)} profiles...")
        self.status_bar.showMessage("Extracting passwords...")

        # Run extraction in a separate thread
        def extract_thread():
            try:
                # Start statistics session
                self.stats_manager.start_session()

                total_profiles = len(selected_profiles)
                all_passwords = []

                for i, profile in enumerate(selected_profiles):
                    # Update progress
                    progress = int((i / total_profiles) * 100)
                    self.update_progress.emit(progress, f"Extracting from {profile.browser_name} - {profile.profile_name}...")

                    # Extract passwords
                    try:
                        passwords = self.password_extractor.extract_passwords_from_profile(profile)
                        all_passwords.extend(passwords)

                        # Track statistics
                        self.stats_manager.add_profile_result(profile.browser_name, len(passwords), False)

                        # Log
                        self.log_message.emit(f"Extracted {len(passwords)} passwords from {profile.browser_name} - {profile.profile_name}")
                    except Exception as profile_error:
                        logger.error(f"Error extracting from {profile}: {profile_error}")
                        self.stats_manager.add_profile_result(profile.browser_name, 0, True)
                        self.log_message.emit(f"Error extracting from {profile.browser_name} - {profile.profile_name}: {profile_error}")

                # Remove duplicates and sort
                unique_passwords = sorted(list(set(all_passwords)))

                # End statistics session
                session = self.stats_manager.end_session(len(unique_passwords))

                # Complete
                self.update_progress.emit(100, "Extraction complete!")
                self.extraction_complete.emit(unique_passwords)

            except Exception as e:
                logger.error(f"Error extracting passwords: {e}")
                self.log_message.emit(f"Error extracting passwords: {e}")
                self.update_progress.emit(0, "Extraction failed!")

                # Re-enable buttons
                QApplication.instance().postEvent(
                    self,
                    EnableButtonsEvent()
                )

        threading.Thread(target=extract_thread).start()

    def save_passwords(self):
        """Save the extracted passwords to a file."""
        # Get the text from the password list
        password_text = self.password_list.toPlainText()

        if not password_text:
            QMessageBox.warning(
                self,
                "No Passwords",
                "There are no passwords to save."
            )
            return

        # Ask for a file name
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Passwords",
            "",
            "Text Files (*.txt);;Encrypted Files (*.enc);;All Files (*)"
        )

        if not file_path:
            return

        try:
            # Check if we should encrypt the file
            encrypt = file_path.endswith('.enc')

            if encrypt:
                # Encrypt the passwords
                passwords = password_text.split('\n')
                encrypted_data = self.encryption.encrypt_password_list(passwords)

                # Write to file
                with open(file_path, 'wb') as f:
                    f.write(encrypted_data)
            else:
                # Write plain text
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(password_text)

            self.log_message.emit(f"Passwords saved to {file_path}")
            self.status_bar.showMessage(f"Passwords saved to {file_path}", 5000)

            QMessageBox.information(
                self,
                "Passwords Saved",
                f"Passwords have been saved to {file_path}"
            )

        except Exception as e:
            logger.error(f"Error saving passwords: {e}")
            self.log_message.emit(f"Error saving passwords: {e}")

            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred while saving passwords: {e}"
            )

    def clear_results(self):
        """Clear the extraction results."""
        self.password_list.clear_passwords()
        self.progress_bar.setValue(0)
        self.save_button.setEnabled(False)
        self.analyze_button.setEnabled(False)
        self.log_message.emit("Results cleared")
        self.status_bar.showMessage("Results cleared", 3000)

    @Slot(int, str)
    def on_progress_update(self, progress: int, message: str):
        """Handle progress updates."""
        self.progress_bar.setValue(progress)
        self.status_bar.showMessage(message)

    @Slot(list)
    def on_extraction_complete(self, passwords: List[str]):
        """Handle extraction completion."""
        # Display passwords
        self.password_list.set_passwords(passwords)

        # Enable buttons
        self.extract_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.analyze_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        self.refresh_button.setEnabled(True)

        # Log
        self.log_message.emit(f"Extraction complete! Found {len(passwords)} unique passwords.")
        self.status_bar.showMessage(f"Extraction complete! Found {len(passwords)} unique passwords.", 5000)

    @Slot(str)
    def on_log_message(self, message: str):
        """Handle log messages."""
        self.log_widget.append_log(message)

    def apply_config(self):
        """Apply configuration settings to the UI."""
        # Apply window size
        width = self.config.get('ui.window_width', 1000)
        height = self.config.get('ui.window_height', 700)
        self.resize(width, height)

    def analyze_passwords(self):
        """Analyze the extracted passwords for strength and patterns."""
        password_text = self.password_list.toPlainText()

        if not password_text:
            QMessageBox.warning(
                self,
                "No Passwords",
                "There are no passwords to analyze."
            )
            return

        passwords = [line.strip() for line in password_text.split('\n') if line.strip()]

        # Perform analysis
        analysis = self.password_analyzer.analyze_password_list(passwords)

        # Show analysis dialog
        self.show_analysis_dialog(analysis)

    def show_analysis_dialog(self, analysis):
        """Show password analysis results in a dialog."""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton

        dialog = QDialog(self)
        dialog.setWindowTitle("Password Analysis Results")
        dialog.setMinimumSize(600, 500)

        layout = QVBoxLayout(dialog)

        # Create analysis text
        analysis_text = f"""Password Analysis Report
========================

Total Passwords: {analysis['total_passwords']}
Unique Passwords: {analysis['unique_passwords']}
Duplicate Rate: {analysis['duplicate_rate']:.1f}%

Average Length: {analysis['average_length']}
Average Entropy: {analysis['average_entropy']:.1f}
Average Strength Score: {analysis['average_strength_score']:.1f}

Strength Distribution:
{self._format_dict(analysis['strength_distribution'])}

Character Usage:
- Uppercase: {analysis['character_usage']['uppercase']:.1f}%
- Lowercase: {analysis['character_usage']['lowercase']:.1f}%
- Digits: {analysis['character_usage']['digits']:.1f}%
- Symbols: {analysis['character_usage']['symbols']:.1f}%

Common Passwords Found: {analysis['common_passwords_found']} ({analysis['common_passwords_rate']:.1f}%)

Length Distribution:
{self._format_dict(analysis['length_distribution'])}

Security Recommendations:
{chr(10).join('- ' + rec for rec in analysis['security_recommendations'])}
"""

        text_widget = QTextEdit()
        text_widget.setPlainText(analysis_text)
        text_widget.setReadOnly(True)
        text_widget.setFont(QFont("Consolas", 10))

        layout.addWidget(text_widget)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.exec()

    def show_statistics(self):
        """Show extraction statistics dialog."""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton

        dialog = QDialog(self)
        dialog.setWindowTitle("Extraction Statistics")
        dialog.setMinimumSize(600, 500)

        layout = QVBoxLayout(dialog)

        # Get statistics
        stats = self.stats_manager.get_summary_stats()
        browser_ranking = self.stats_manager.get_browser_ranking()

        # Create statistics text
        stats_text = f"""Extraction Statistics
====================

Total Extractions: {stats['total_extractions']}
Total Passwords Found: {stats['total_passwords_found']}
Total Profiles Scanned: {stats['total_profiles_scanned']}
Average Passwords per Session: {stats['average_passwords_per_session']}
Total Time Spent: {stats['total_time_spent_hours']} hours
Most Productive Browser: {stats['most_productive_browser']}
Last Extraction: {stats['last_extraction']}

Recent Activity (Last 7 Days):
- Sessions: {stats['recent_sessions_count']}
- Passwords Found: {stats['recent_passwords_found']}

Browser Ranking (by passwords found):
{self._format_browser_ranking(browser_ranking)}

Average Session Duration: {stats['average_session_duration']} seconds
"""

        text_widget = QTextEdit()
        text_widget.setPlainText(stats_text)
        text_widget.setReadOnly(True)
        text_widget.setFont(QFont("Consolas", 10))

        layout.addWidget(text_widget)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.exec()

from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QSpinBox, QCheckBox, QComboBox, QPushButton, QHBoxLayout, QLabel

    def show_settings(self):
        """Show settings dialog with configurable options."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.setMinimumSize(600, 400)

        layout = QFormLayout(dialog)

        # UI Settings
        window_width_spin = QSpinBox()
        window_width_spin.setRange(800, 3840)
        window_width_spin.setValue(self.config.get('ui.window_width', 1000))

        window_height_spin = QSpinBox()
        window_height_spin.setRange(600, 2160)
        window_height_spin.setValue(self.config.get('ui.window_height', 700))

        remember_size_checkbox = QCheckBox("Remember window size")
        remember_size_checkbox.setChecked(self.config.get('ui.remember_window_size', True))

        theme_combo = QComboBox()
        theme_combo.addItems(['default', 'dark', 'light'])
        theme_combo.setCurrentText(self.config.get('ui.theme', 'default'))

        # Extraction Settings
        auto_detect_checkbox = QCheckBox("Auto-detect browser profiles on startup")
        auto_detect_checkbox.setChecked(self.config.get('extraction.auto_detect_profiles', True))

        include_empty_checkbox = QCheckBox("Include empty passwords in extraction")
        include_empty_checkbox.setChecked(self.config.get('extraction.include_empty_passwords', False))

        max_password_length_spin = QSpinBox()
        max_password_length_spin.setRange(1, 10000)
        max_password_length_spin.setValue(self.config.get('extraction.max_password_length', 1000))

        timeout_spin = QSpinBox()
        timeout_spin.setRange(5, 300)
        timeout_spin.setValue(self.config.get('extraction.timeout_seconds', 30))

        retry_spin = QSpinBox()
        retry_spin.setRange(0, 10)
        retry_spin.setValue(self.config.get('extraction.retry_attempts', 3))

        # Security Settings
        auto_encrypt_checkbox = QCheckBox("Automatically encrypt saved password files")
        auto_encrypt_checkbox.setChecked(self.config.get('security.auto_encrypt_saves', True))

        clear_clipboard_spin = QSpinBox()
        clear_clipboard_spin.setRange(0, 300)
        clear_clipboard_spin.setValue(self.config.get('security.clear_clipboard_after', 60))

        secure_delete_checkbox = QCheckBox("Securely delete temporary files after use")
        secure_delete_checkbox.setChecked(self.config.get('security.secure_delete_temp_files', True))

        # Export Settings
        default_format_combo = QComboBox()
        default_format_combo.addItems(['txt', 'enc', 'csv', 'json'])
        default_format_combo.setCurrentText(self.config.get('export.default_format', 'txt'))

        include_metadata_checkbox = QCheckBox("Include metadata in exported files")
        include_metadata_checkbox.setChecked(self.config.get('export.include_metadata', False))

        sort_alpha_checkbox = QCheckBox("Sort passwords alphabetically on export")
        sort_alpha_checkbox.setChecked(self.config.get('export.sort_alphabetically', True))

        remove_duplicates_checkbox = QCheckBox("Remove duplicate passwords on export")
        remove_duplicates_checkbox.setChecked(self.config.get('export.remove_duplicates', True))

        # Add widgets to layout
        layout.addRow("Window Width:", window_width_spin)
        layout.addRow("Window Height:", window_height_spin)
        layout.addRow("", remember_size_checkbox)
        layout.addRow("Theme:", theme_combo)

        layout.addRow("", QLabel("<b>Extraction Settings</b>"))
        layout.addRow("", auto_detect_checkbox)
        layout.addRow("", include_empty_checkbox)
        layout.addRow("Max Password Length:", max_password_length_spin)
        layout.addRow("Timeout (seconds):", timeout_spin)
        layout.addRow("Retry Attempts:", retry_spin)

        layout.addRow("", QLabel("<b>Security Settings</b>"))
        layout.addRow("", auto_encrypt_checkbox)
        layout.addRow("Clear Clipboard After (seconds):", clear_clipboard_spin)
        layout.addRow("", secure_delete_checkbox)

        layout.addRow("", QLabel("<b>Export Settings</b>"))
        layout.addRow("Default Export Format:", default_format_combo)
        layout.addRow("", include_metadata_checkbox)
        layout.addRow("", sort_alpha_checkbox)
        layout.addRow("", remove_duplicates_checkbox)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addRow(button_layout)

        def on_save():
            # Save UI settings
            self.config.set('ui.window_width', window_width_spin.value())
            self.config.set('ui.window_height', window_height_spin.value())
            self.config.set('ui.remember_window_size', remember_size_checkbox.isChecked())
            self.config.set('ui.theme', theme_combo.currentText())

            # Save extraction settings
            self.config.set('extraction.auto_detect_profiles', auto_detect_checkbox.isChecked())
            self.config.set('extraction.include_empty_passwords', include_empty_checkbox.isChecked())
            self.config.set('extraction.max_password_length', max_password_length_spin.value())
            self.config.set('extraction.timeout_seconds', timeout_spin.value())
            self.config.set('extraction.retry_attempts', retry_spin.value())

            # Save security settings
            self.config.set('security.auto_encrypt_saves', auto_encrypt_checkbox.isChecked())
            self.config.set('security.clear_clipboard_after', clear_clipboard_spin.value())
            self.config.set('security.secure_delete_temp_files', secure_delete_checkbox.isChecked())

            # Save export settings
            self.config.set('export.default_format', default_format_combo.currentText())
            self.config.set('export.include_metadata', include_metadata_checkbox.isChecked())
            self.config.set('export.sort_alphabetically', sort_alpha_checkbox.isChecked())
            self.config.set('export.remove_duplicates', remove_duplicates_checkbox.isChecked())

            # Persist config to file
            self.config.save_config()

            # Apply UI changes immediately if needed
            if remember_size_checkbox.isChecked():
                self.resize(window_width_spin.value(), window_height_spin.value())

            # TODO: Apply theme changes dynamically if implemented

            dialog.accept()

        def on_cancel():
            dialog.reject()

        save_button.clicked.connect(on_save)
        cancel_button.clicked.connect(on_cancel)

        dialog.exec()

    def _format_dict(self, d):
        """Format a dictionary for display."""
        return '\n'.join(f"  {k}: {v}" for k, v in d.items())

    def _format_browser_ranking(self, ranking):
        """Format browser ranking for display."""
        if not ranking:
            return "  No data available"

        result = []
        for i, (browser, stats) in enumerate(ranking[:10], 1):
            result.append(f"  {i}. {browser}: {stats['total_passwords']} passwords")
        return '\n'.join(result)

# Custom events for thread communication

class UpdateProfilesEvent(QEvent):
    """Custom event to update profiles from a thread."""

    EVENT_TYPE = QEvent.Type(QEvent.registerEventType())

    def __init__(self, profiles):
        super().__init__(self.EVENT_TYPE)
        self.profiles = profiles

    def type(self):
        return self.EVENT_TYPE

class EnableButtonsEvent(QEvent):
    """Custom event to enable buttons from a thread."""

    EVENT_TYPE = QEvent.Type(QEvent.registerEventType())

    def __init__(self):
        super().__init__(self.EVENT_TYPE)

    def type(self):
        return self.EVENT_TYPE

# Override event method to handle custom events
def event(self, event):
    if event.type() == UpdateProfilesEvent.EVENT_TYPE:
        self.profile_list.set_profiles(event.profiles)
        self.log_message.emit(f"Detected {len(event.profiles)} browser profiles")
        self.status_bar.showMessage(f"Detected {len(event.profiles)} browser profiles", 5000)
        return True
    elif event.type() == EnableButtonsEvent.EVENT_TYPE:
        self.extract_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        self.refresh_button.setEnabled(True)
        return True
    return super(MainWindow, self).event(event)

# Add the event method to the MainWindow class
MainWindow.event = event
