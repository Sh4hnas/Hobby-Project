# AI Image Generator Backend

A FastAPI backend service that generates images of famous people or cartoon characters similar to uploaded photos using AI face recognition and image processing.

## Features

- **Image Upload**: Secure file upload with validation
- **Face Detection**: Automatic face detection using OpenCV
- **Famous Person Matching**: Find similar celebrities using InsightFace
- **Cartoon Generation**: Multiple cartoon styles (anime, comic, cartoon, sketch)
- **RESTful API**: Clean API endpoints with proper error handling

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **OpenCV**: Computer vision library for image processing
- **InsightFace**: State-of-the-art face recognition library
- **Pillow**: Python Imaging Library for image manipulation
- **NumPy**: Numerical computing library

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create necessary directories**:
   The application will automatically create the following directories:
   - `uploads/`: For storing uploaded images
   - `generated/`: For storing generated images
   - `data/celebrities/`: For celebrity database

## Usage

### Starting the Server

```bash
# Option 1: Using the run script
python run.py

# Option 2: Direct execution
python main.py

# Option 3: Using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## API Endpoints

### 1. Upload Image
```
POST /upload-image
```
Upload an image for processing.

**Parameters:**
- `file`: Image file (multipart/form-data)

**Response:**
```json
{
  "message": "Image uploaded successfully",
  "filename": "uuid.jpg",
  "file_path": "/path/to/uploaded/image.jpg"
}
```

### 2. Generate Famous Person
```
POST /generate-famous-person
```
Generate an image of a famous person similar to the uploaded image.

**Parameters:**
- `filename`: Name of the uploaded image file

**Response:**
```json
{
  "message": "Famous person image generated successfully",
  "result_path": "/path/to/generated/image.jpg",
  "filename": "famous_person_uuid.jpg"
}
```

### 3. Generate Cartoon
```
POST /generate-cartoon
```
Generate a cartoon version of the uploaded image.

**Parameters:**
- `filename`: Name of the uploaded image file
- `style`: Cartoon style (optional, default: "cartoon")
  - Available styles: "anime", "comic", "cartoon", "sketch"

**Response:**
```json
{
  "message": "Cartoon image generated successfully",
  "result_path": "/path/to/generated/image.jpg",
  "filename": "cartoon_uuid.jpg"
}
```

### 4. Download Image
```
GET /download/{filename}
```
Download a generated image.

### 5. Health Check
```
GET /health
```
Check if the service is running.

## Configuration

Edit `config.py` to modify:
- API host and port
- File upload limits
- Allowed file extensions
- AI model settings

## Project Structure

```
backend/
├── main.py                 # FastAPI application
├── run.py                  # Server startup script
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── services/             # Service modules
│   ├── __init__.py
│   ├── image_processor.py    # Basic image operations
│   ├── face_matcher.py       # Face recognition and matching
│   └── cartoon_generator.py  # Cartoon style generation
├── uploads/              # Uploaded images (auto-created)
├── generated/            # Generated images (auto-created)
└── data/                 # Data directory
    └── celebrities/      # Celebrity database
```

## Development

### Adding New Cartoon Styles

1. Add a new method to `CartoonGenerator` class
2. Register it in the `cartoon_styles` dictionary
3. Update the `CARTOON_STYLES` list in `config.py`

### Adding New Celebrities

1. Add celebrity images to `data/celebrities/`
2. Update the `famous_people_db` in `FaceMatcher`

### Error Handling

The API includes comprehensive error handling for:
- Invalid file types
- Missing faces in images
- File size limits
- Processing errors

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed
2. **Face detection fails**: Ensure the uploaded image contains a clear face
3. **Memory issues**: Reduce image size or increase system memory
4. **Model loading errors**: Check if InsightFace models are properly downloaded

### Logs

Check the console output for detailed error messages and processing logs.

## License

This project is part of the AI Image Generator application.