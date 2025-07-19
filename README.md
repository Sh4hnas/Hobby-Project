# AI Celebrity Generator

An AI-powered web application that analyzes user photos and generates images with high similarity to famous celebrities or cartoon characters.

## Features

- 📸 **Photo Upload**: Drag and drop or click to upload your photo
- 🎭 **Celebrity Matching**: AI analyzes your face and finds similar celebrities
- 🎨 **Style Generation**: Choose between realistic or cartoon styles
- ⚡ **Real-time Processing**: Fast face recognition and image generation
- 📱 **Responsive Design**: Beautiful UI that works on all devices
- 🔄 **Multiple Options**: Try different celebrities and styles

## Technology Stack

### Frontend
- **React 18** - Modern UI framework
- **Tailwind CSS** - Utility-first CSS framework
- **React Dropzone** - File upload component
- **Axios** - HTTP client for API requests

### Backend
- **Flask** - Python web framework
- **OpenCV** - Computer vision library
- **face-recognition** - Face detection and encoding
- **PIL (Pillow)** - Image processing
- **NumPy** - Numerical computations

### AI/ML Components
- Face recognition and encoding
- Similarity matching algorithms
- Image style transfer (placeholder for advanced models)
- Future integration ready for:
  - Stable Diffusion
  - StyleGAN
  - Custom trained models

## Installation

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- pip (Python package manager)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
npm install
```

2. Install Tailwind CSS:
```bash
npx tailwindcss init -p
```

## Usage

### Development Mode

1. Start the backend server:
```bash
cd backend
python app.py
```

2. In a new terminal, start the frontend:
```bash
npm start
```

3. Open your browser and navigate to `http://localhost:3000`

### Production Mode

1. Build the frontend:
```bash
npm run build
```

2. Serve the built files with your preferred web server

## How It Works

1. **Upload**: User uploads a photo through the web interface
2. **Analysis**: Backend extracts face encodings using face-recognition library
3. **Matching**: AI compares the user's face with celebrity database
4. **Selection**: User chooses from similar celebrities and preferred style
5. **Generation**: AI generates a stylized image (currently using basic image processing, ready for advanced models)
6. **Results**: User sees the original, celebrity reference, and generated image

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/upload` - Upload and analyze photo
- `POST /api/generate` - Generate celebrity-style image
- `GET /api/image/<filename>` - Retrieve generated images
- `GET /api/celebrities` - Get celebrity database

## Project Structure

```
ai-celebrity-generator/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── uploads/           # User uploaded images
│   ├── generated/         # AI generated images
│   └── celebrity_db/      # Celebrity reference images
├── src/
│   ├── App.js             # Main React component
│   ├── App.css           # Component styles
│   ├── index.js          # React entry point
│   └── index.css         # Global styles
├── public/
│   └── index.html        # HTML template
├── package.json          # Node.js dependencies
├── tailwind.config.js    # Tailwind configuration
└── README.md            # Project documentation
```

## Future Enhancements

- **Advanced AI Models**: Integration with Stable Diffusion, StyleGAN, or custom models
- **Real Celebrity Database**: Actual celebrity photos for better matching
- **User Accounts**: Save generated images and history
- **Social Sharing**: Share results on social media
- **Mobile App**: React Native version
- **Batch Processing**: Process multiple photos at once
- **Custom Styles**: More artistic and creative styles
- **3D Generation**: 3D avatar creation

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for inspiration in AI image generation
- The face-recognition library contributors
- React and Flask communities
- All the amazing open-source projects that made this possible

## Disclaimer

This project is for educational and entertainment purposes. The AI-generated images are approximations and should not be used for identity verification or any official purposes. Please respect privacy and copyright when using celebrity likenesses.
