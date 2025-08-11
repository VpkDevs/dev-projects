# Haunted HLS Downloader

A haunted electro-vaporwave baroque futurist desktop application for downloading HLS (HTTP Live Streaming) videos with a stunning maximalist aesthetic.

## Features

### Core Functionality
- **Real HLS Downloading**: Parse M3U8 files and download video segments
- **Quality Selection**: Analyze and choose from multiple video qualities
- **Browser Detection**: Automatically detect installed browsers and scan for HLS streams
- **Batch Processing**: Download multiple streams simultaneously
- **FFmpeg Integration**: Merge segments into high-quality MP4 files

### Aesthetic Features
- **Haunted Electro-Vaporwave Design**: Dark, neon-accented interface with retro-futuristic elements
- **Baroque Ornamental Details**: Decorative elements with a digital twist
- **3D Animations**: Three.js powered background with floating geometric shapes
- **Particle Effects**: Interactive particle systems that respond to user input
- **Glitch Effects**: Text glitch animations and visual distortions
- **Maximalist UI**: Over-the-top visual effects with neon glows and animations

### Technical Features
- **Cross-Platform**: Built with Electron for Windows, macOS, and Linux
- **Real-time Progress**: Live download progress with segment and merge tracking
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Cancellation Support**: Ability to cancel downloads mid-process
- **Validation**: URL validation and stream analysis before download

## Installation

### Prerequisites
- Node.js (v14 or higher)
- FFmpeg (must be installed and available in PATH)
- Git

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd haunted-hls-downloader
```

2. Install dependencies:
```bash
npm install
```

3. Install FFmpeg:
   - **Windows**: Download from https://ffmpeg.org/download.html and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) or equivalent

4. Run the application:
```bash
npm start
```

## Usage

### Browser Detection
1. Click "SCAN BROWSERS" to detect installed browsers
2. Select a browser to view available HLS streams
3. Choose a stream from the detected list

### Manual URL Entry
1. Enter an M3U8 URL in the input field
2. Click "ADD URL" to validate and analyze the stream
3. Select desired quality from the quality selector

### Download Process
1. Choose output directory using "Browse" button
2. Set filename (will auto-update based on quality selection)
3. Click "DOWNLOAD" to start the process
4. Monitor progress through the real-time progress bars
5. Cancel anytime using the "CANCEL" button

### Quality Selection
- **Automatic**: Best quality selected by default
- **Manual**: Choose from available resolutions and bitrates
- **Metrics**: View stream duration, codecs, and other metadata

## Architecture

### Main Components

#### `src/hlsDownloader.js`
- Core HLS downloading functionality
- M3U8 parsing and segment extraction
- Parallel segment downloading with concurrency control
- FFmpeg integration for video merging
- Event-driven progress reporting

#### `src/browserDetector.js`
- Cross-platform browser detection
- Session file parsing for Chrome, Firefox, Edge
- HLS stream identification in browser tabs
- Tab content analysis and URL extraction

#### `src/qualitySelector.js`
- M3U8 quality analysis
- Bandwidth and resolution parsing
- Quality recommendation engine
- Stream metrics calculation

#### `main.js`
- Electron main process
- IPC communication handlers
- File system operations
- Window management

#### `renderer.js`
- Frontend application logic
- UI event handling
- Three.js 3D animations
- Real-time progress updates

#### `styles.css`
- Haunted electro-vaporwave aesthetic
- CSS animations and transitions
- Responsive grid layout
- Neon glow effects and gradients

## Supported Platforms

### Browsers
- Google Chrome / Chromium
- Mozilla Firefox
- Microsoft Edge
- Opera
- Brave Browser

### Operating Systems
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu, Debian, Fedora, etc.)

### Video Formats
- HLS (HTTP Live Streaming) - .m3u8
- Multiple quality streams
- Various codecs (H.264, H.265, etc.)

## Configuration

### Default Settings
- Output format: MP4
- Concurrent downloads: 5 segments
- Default quality: Highest available
- Timeout: 30 seconds per segment

### Customization
Settings can be modified in the source code:
- Concurrency limit in `hlsDownloader.js`
- UI colors in CSS variables
- Animation speeds and effects
- Browser detection paths

## Troubleshooting

### Common Issues

**FFmpeg not found**
- Ensure FFmpeg is installed and in system PATH
- Test with `ffmpeg -version` in terminal

**Browser detection fails**
- Check browser installation paths
- Ensure browsers are properly closed before scanning
- Some browsers may require additional permissions

**Download errors**
- Verify M3U8 URL is accessible
- Check network connectivity
- Ensure sufficient disk space

**UI not loading**
- Clear Electron cache
- Check console for JavaScript errors
- Verify all dependencies are installed

### Performance Tips
- Close unnecessary browser tabs before scanning
- Use SSD storage for faster segment processing
- Increase concurrency for faster downloads (modify source)
- Select appropriate quality for your bandwidth

## Development

### Building from Source
```bash
# Development mode
npm run dev

# Production build
npm run build

# Package for distribution
npm run dist
```

### Code Structure
- `/src/` - Core functionality modules
- `/assets/` - Icons and static resources
- `main.js` - Electron main process
- `renderer.js` - Frontend application
- `styles.css` - UI styling and animations

### Contributing
1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

## License

This project is licensed under the ISC License.

## Acknowledgments

- Three.js for 3D graphics
- Electron for cross-platform desktop apps
- FFmpeg for video processing
- The vaporwave aesthetic community for inspiration
