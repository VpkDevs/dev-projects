# Passwordz - Advanced Password Extraction Tool

Passwordz is a powerful and user-friendly application designed to extract passwords from Google Password Manager across multiple browsers and Windows user accounts. It offers advanced features such as password analysis, statistics tracking, encryption, and multi-threaded operations, all wrapped in a sleek graphical user interface.

## Features

### Core Functionality
- Extract passwords from Google Password Manager for a wide range of browsers and profiles.
- Support for multiple browser profiles and Windows user accounts.
- Consolidate extracted passwords into an organized, alphabetical list.
- User-friendly GUI with responsive design and progress feedback.
- Robust input validation and error handling for reliability.
- AES-256 encryption for secure storage of password data.

### Advanced Features
- Comprehensive password strength analysis with detailed reports.
- Extraction statistics and browser performance metrics.
- Configurable settings with persistent storage.
- Multi-threaded operations to keep the UI responsive.
- Detailed logging for troubleshooting and auditing.
- Export options including plain text, encrypted files, CSV, and JSON.

## Supported Browsers

- Google Chrome (including Dev and Canary)
- Microsoft Edge (including Dev and Canary)
- Brave Browser
- Mozilla Firefox (limited support)
- Opera (including GX and One)
- Vivaldi
- Yandex Browser
- AVG Secure Browser
- CCleaner Browser
- Naver Whale

## Requirements

- Windows operating system
- Python 3.8 or higher
- PySide6 (Qt for Python)
- PyWin32
- Cryptography

## Installation

1. Clone or download the repository.
2. Install dependencies using:

   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application with:

```
python main.py
```

### Extracting Passwords

1. Launch the app.
2. Select browser profiles to extract from.
3. Click "Extract Passwords".
4. View and save extracted passwords (plain text or encrypted).

### Password Analysis

- Analyze password strength, character usage, common passwords, and entropy.
- View detailed reports via the "Analyze Passwords" button.

### Statistics

- View extraction history, browser rankings, and session metrics.

### Configuration

- Access the settings dialog to customize UI, extraction, security, and export options.
- Settings are saved automatically.

## Security Considerations

- Passwords are stored only in memory during extraction.
- Option to save passwords in encrypted format.
- Temporary files are securely deleted.
- No association with usernames or websites to protect privacy.

## Project Structure

- `main.py`: Application entry point.
- `gui.py`: Graphical user interface.
- `browser_detector.py`: Detects installed browsers and profiles.
- `password_extractor.py`: Core password extraction logic.
- `encryption.py`: Encryption and decryption utilities.
- `config.py`: Configuration management.
- `extraction_stats.py`: Statistics tracking.
- `password_analyzer.py`: Password strength analysis.
- `utils.py`: Helper functions.
- `test_app.py`: Test suite.

## Limitations

- Firefox extraction limited due to encryption.
- Browsers must be closed for full extraction.
- Some antivirus software may interfere.

## License and Disclaimer

This tool is for educational and legitimate use only. Unauthorized use is illegal and unethical. The developers are not liable for misuse.

Please use responsibly and only on systems you own or have permission to access.

---

For more information, issues, or contributions, please visit the project repository.
