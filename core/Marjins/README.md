# Marjins - Window Manager

A C# WPF utility that automatically resizes and positions all open windows with customizable margins using global hotkeys.

## Features

- **Global Hotkey**: Press `Ctrl + Alt + M` to instantly resize all windows
- **Customizable Margins**: Set individual margins for left, top, right, and bottom
- **System Tray Integration**: Minimize to tray to keep hotkey active in background
- **Window Management**: Automatically handles window restoration from minimized state
- **Smart Filtering**: Skips system windows, taskbar, and other non-user windows
- **Real-time Window List**: View all manageable windows in the interface

## Usage

1. **Launch the Application**: Run `Marjins.exe`
2. **Configure Margins**: Set your desired margins in pixels (default: 50px all around)
3. **Use Hotkey**: Press `Ctrl + Alt + M` anywhere in Windows to resize all windows
4. **Manual Resize**: Click "Resize All Windows Now" button in the interface
5. **System Tray**: Minimize the app to system tray to keep it running in background

## How It Works

When triggered, Marjins will:
1. Enumerate all top-level visible windows
2. Filter out system windows (taskbar, desktop, etc.)
3. Calculate target size based on screen dimensions minus margins
4. Restore minimized windows and resize them to fill the available space
5. Position all windows with the specified margins

## Requirements

- Windows 10 or later
- .NET 8.0 Runtime
- Administrator privileges may be required for some applications

## Building

```bash
dotnet build --configuration Release
```

## Installation

1. Download or clone the repository
2. Build the solution using .NET 8.0
3. Run the executable
4. Optionally, create a shortcut in your startup folder for automatic launch

## Configuration

The application saves your margin preferences and will remember them between sessions. The hotkey is currently fixed to `Ctrl + Alt + M` but can be modified in the source code.

## Limitations

- Some applications may not respond to resize requests due to their own window management
- System-protected windows cannot be resized
- The utility works best with standard desktop applications

## License

This project is open source. Feel free to modify and distribute as needed.
