# AI Image Generator

An AI-powered web application that generates images of famous people or cartoon characters similar to uploaded photos using advanced face recognition and image processing techniques.

## 🎯 Features

- **Smart Face Detection**: Automatically detects faces in uploaded images
- **Famous Person Matching**: Finds celebrities with similar facial features using InsightFace
- **Multiple Cartoon Styles**: Generate cartoons in different styles (anime, comic, cartoon, sketch)
- **Real-time Processing**: Fast image processing with progress feedback
- **Modern Web Interface**: Beautiful, responsive UI built with React
- **RESTful API**: Clean, well-documented API endpoints

## 🏗️ Architecture

The project consists of two main components:

### Backend (FastAPI)
- **Face Recognition**: Uses InsightFace for accurate face detection and matching
- **Image Processing**: OpenCV and Pillow for image manipulation
- **Cartoon Generation**: Multiple artistic filters and effects
- **File Management**: Secure upload/download with validation

### Frontend (React) - Coming Soon
- **Modern UI**: Beautiful, responsive interface
- **Drag & Drop**: Easy image upload
- **Real-time Preview**: See results instantly
- **Multiple Styles**: Choose from various cartoon effects

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+ (for frontend)
- Git

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-image-generator
   ```

2. **Start the backend**:
   ```bash
   # Option 1: Use the startup script (recommended)
   ./start_backend.sh
   
   # Option 2: Manual setup
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python run.py
   ```

3. **Verify the backend is running**:
   - Open http://localhost:8000/docs for interactive API documentation
   - Open http://localhost:8000/health for health check

### Frontend Setup (Coming Soon)

```bash
cd frontend
npm install
npm start
```

## 📖 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/health` | Health check |
| `POST` | `/upload-image` | Upload an image |
| `POST` | `/generate-famous-person` | Generate famous person match |
| `POST` | `/generate-cartoon` | Generate cartoon version |
| `GET` | `/download/{filename}` | Download generated image |

### Example Usage

```bash
# Upload an image
curl -X POST "http://localhost:8000/upload-image" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_photo.jpg"

# Generate cartoon
curl -X POST "http://localhost:8000/generate-cartoon" \
  -H "accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "filename=uploaded_image.jpg&style=anime"

# Generate famous person match
curl -X POST "http://localhost:8000/generate-famous-person" \
  -H "accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "filename=uploaded_image.jpg"
```

## 🎨 Cartoon Styles

The application supports multiple cartoon styles:

- **Anime**: Japanese animation style with smooth shading
- **Comic**: Comic book style with bold outlines
- **Cartoon**: Classic cartoon effect with enhanced colors
- **Sketch**: Pencil sketch artistic effect

## 🔧 Configuration

Edit `backend/config.py` to customize:

- API host and port
- File upload limits
- Allowed file extensions
- AI model settings
- Similarity thresholds

## 📁 Project Structure

```
ai-image-generator/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application
│   ├── run.py              # Server startup script
│   ├── config.py           # Configuration
│   ├── requirements.txt    # Python dependencies
│   ├── services/           # Core services
│   │   ├── image_processor.py
│   │   ├── face_matcher.py
│   │   └── cartoon_generator.py
│   ├── uploads/            # Uploaded images
│   ├── generated/          # Generated images
│   └── data/               # Data directory
│       └── celebrities/    # Celebrity database
├── frontend/               # React frontend (coming soon)
├── start_backend.sh        # Backend startup script
└── README.md              # This file
```

## 🧪 Testing

Run the test suite to verify everything works:

```bash
cd backend
python test_api.py
```

## 🔍 Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Face detection fails**: Ensure the uploaded image contains a clear, front-facing face

3. **Memory issues**: Reduce image size or increase system memory

4. **Model loading errors**: InsightFace models are downloaded automatically on first use

### Logs

Check the console output for detailed error messages and processing logs.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [InsightFace](https://github.com/deepinsight/insightface) for face recognition
- [OpenCV](https://opencv.org/) for computer vision
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Pillow](https://python-pillow.org/) for image processing

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section
2. Review the API documentation at http://localhost:8000/docs
3. Open an issue on GitHub

---

**Happy image generating! 🎨✨**
