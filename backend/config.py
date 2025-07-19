import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Upload and generated directories
UPLOAD_DIR = BASE_DIR.parent / "uploads"
GENERATED_DIR = BASE_DIR.parent / "generated"
DATA_DIR = BASE_DIR / "data"
CELEBRITY_DIR = DATA_DIR / "celebrities"

# Create directories if they don't exist
UPLOAD_DIR.mkdir(exist_ok=True)
GENERATED_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
CELEBRITY_DIR.mkdir(exist_ok=True)

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# File upload settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}

# AI Model settings
INSIGHTFACE_MODEL = "buffalo_l"
FACE_DETECTION_SIZE = (640, 640)

# Cartoon generation settings
DEFAULT_CARTOON_STYLE = "cartoon"
CARTOON_STYLES = ["anime", "comic", "cartoon", "sketch"]

# Similarity threshold for face matching
SIMILARITY_THRESHOLD = 0.6