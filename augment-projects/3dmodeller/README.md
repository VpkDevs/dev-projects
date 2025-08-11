# GameAssetForge

A comprehensive AI-powered game asset creation suite that allows you to generate, optimize, and manage 3D models for video games.

## Features

### Advanced Asset Generation
- Generate individual 3D models from text descriptions
- Create entire asset sets with batch generation (environments, characters, etc.)
- Choose from multiple art styles with consistent aesthetics
- Apply style presets to maintain visual coherence across your game

### Game-Ready Optimization
- Automatically optimize models for specific game engines (Unity, Unreal, Godot)
- Reduce polygon count while preserving visual quality
- Optimize textures for better performance
- Generate PBR maps for realistic materials

### Asset Management
- Organize models into projects
- Build a reusable asset library
- Track generation history
- Export in various formats (GLB, FBX, OBJ, USDZ)

### Real-time Preview
- View 3D models in real-time with interactive controls
- Examine models from all angles
- Test different lighting conditions

## Technologies Used

- **Frontend**: React with Vite, React Router for navigation
- **State Management**: Zustand for global state
- **3D Rendering**: Three.js, React Three Fiber, and Drei
- **API Integration**: Meshy AI API for text-to-3D model generation
- **Styling**: Tailwind CSS for responsive design
- **Storage**: IndexedDB for local asset management
- **Utilities**: JSZip for game engine exports

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Meshy AI API key (sign up at [meshy.ai](https://www.meshy.ai))

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/GameAssetForge.git
   cd GameAssetForge
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Create a `.env` file in the root directory and add your Meshy AI API key:

   ```env
   VITE_MESHY_API_KEY=your_meshy_api_key_here
   ```

4. Start the development server:

   ```bash
   npm run dev
   ```

5. Open your browser and navigate to `http://localhost:5173`

## Usage

### Single Model Generation

1. Navigate to the "Single Model" tab
2. Enter a text description of the 3D model you want to create
3. Select an art style (realistic or sculpture)
4. Enable PBR maps if desired (not available for sculpture style)
5. Click "Generate 3D Model"
6. Wait for the model to be generated (this may take a few minutes)
7. View and interact with the 3D model
8. Optimize the model for your target game engine
9. Download the model in your preferred format

### Batch Generation

1. Navigate to the "Batch Generation" tab
2. Choose a batch type (custom, environment set, or character set)
3. For custom batches:
   - Enter a theme (e.g., "Medieval Weapons")
   - Add variations (one per line, e.g., "Sword", "Shield", "Axe")
4. For environment or character sets, select a predefined type
5. Choose a style preset for consistent aesthetics
6. Click "Generate Batch"
7. Monitor progress in the batch jobs list
8. View and download completed models

### Asset Library

1. Navigate to the "Asset Library" tab
2. Create a new project or select an existing one
3. View all assets in the selected project
4. Organize and categorize your assets

### Style Presets

1. Navigate to the "Style Presets" tab
2. Select from predefined style presets or create your own
3. Customize style settings including:
   - Art style (realistic or sculpture)
   - PBR maps
   - Target game engine
   - Optimization settings

## Building for Production

To build the application for production:

```bash
npm run build
```

The built files will be in the `dist` directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Meshy AI](https://www.meshy.ai) for the text-to-3D API
- [Three.js](https://threejs.org) for 3D rendering
- [React Three Fiber](https://github.com/pmndrs/react-three-fiber) for React integration with Three.js
- [Zustand](https://github.com/pmndrs/zustand) for state management
- [Tailwind CSS](https://tailwindcss.com) for styling
