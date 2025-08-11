# AI Coding Agent Instructions for Marjins

## Project Overview
Marjins is a C# WPF window management utility that resizes all open windows with customizable margins via global hotkeys. The architecture centers around three core components:

- **WindowManager**: Static utility for Win32 window enumeration and manipulation
- **GlobalHotkey**: Win32 hotkey registration and event handling  
- **MainWindow**: WPF UI with system tray integration and MVVM pattern

## Architecture Patterns

### Win32 Interop Layer
The project heavily uses P/Invoke for Win32 APIs. All window operations go through `WindowManager.cs`:
- `EnumWindows()` + `IsValidWindow()` filter for top-level windows only
- `SetWindowPos()` with `SWP_NOZORDER | SWP_NOACTIVATE` flags to avoid focus stealing
- Custom `RECT` struct and `WindowInfo` class for window metadata
- System window filtering via process names (`explorer`, `dwm`) and titles (`Program Manager`)

### WPF Integration Points
- **Hotkey Integration**: `MainWindow` creates window handle via `WindowInteropHelper`, registers with `GlobalHotkey`, processes `WM_HOTKEY` in `WndProc()`
- **System Tray**: `NotifyIcon` from WinForms with context menu for background operation
- **Data Binding**: `ObservableCollection<WindowDisplayInfo>` bound to `ListBox` for window list UI
- **Window State Management**: Override `OnClosing()` to minimize to tray instead of closing

### Core Workflow
1. `ResizeAllWindows()` → `WindowManager.GetTopLevelWindows()` → filter via `ShouldSkipWindow()`
2. Calculate target dimensions: `screenDimensions - margins`
3. For each valid window: restore if minimized, then `SetWindowPos()`

## Critical Development Patterns

### Error Handling
- UI operations wrapped in try-catch with `UpdateStatus()` user feedback
- Win32 API calls return gracefully (don't crash on invalid handles)
- Process enumeration catches exceptions for inaccessible processes

### Testing Architecture
- **WindowManagerTests**: Uses real Win32 `CreateWindowEx()` for integration testing
- **MainWindowIntegrationTests**: STA thread setup required for WPF components
- **Performance constraints**: Window enumeration must complete within 2 seconds
- Test files use xUnit + FluentAssertions pattern

### Build & Dependencies
```powershell
# Standard commands
dotnet build --configuration Release
dotnet test                               # Runs test suite
./run-tests.ps1 -Coverage               # Custom test script with coverage
```

**Critical**: Enable both `UseWPF` and `UseWindowsForms` in project file - WPF for UI, WinForms for `NotifyIcon`

## Common Implementation Gotchas

### Window Filtering Logic
- Child windows filtered by checking `GetWindow(hWnd, GW_OWNER) != IntPtr.Zero`
- Invisible windows filtered before enumeration callback
- Application's own window filtered in UI list by title matching "Marjins"

### Hotkey Registration
- Must use `WindowInteropHelper(this).Handle` after window initialization
- Handle `SourceInitialized` event if window handle not ready
- Dispose pattern critical - hotkeys persist until explicitly unregistered

### System Tray Behavior
- `_isClosing` flag distinguishes user close vs minimize-to-tray
- Window state changes trigger tray balloon notifications
- Context menu provides alternative to double-click restoration

## Key Files for Understanding
- `WindowManager.cs`: All Win32 interop and core window logic
- `MainWindow.xaml.cs`: WPF lifecycle, hotkey integration, tray handling
- `GlobalHotkey.cs`: Win32 hotkey registration pattern
- `run-tests.ps1`: Custom test execution with coverage options

When modifying window logic, always test with system windows (Task Manager, Windows Settings) to verify filtering works correctly.
