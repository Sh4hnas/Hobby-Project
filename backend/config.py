import os
from datetime import timedelta

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    GENERATED_FOLDER = 'generated'
    CELEBRITY_DB_FOLDER = 'celebrity_db'
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # AI model configuration
    FACE_RECOGNITION_TOLERANCE = 0.6
    MAX_CELEBRITIES_RETURNED = 5
    
    # Image processing configuration
    MAX_IMAGE_SIZE = (1024, 1024)
    THUMBNAIL_SIZE = (256, 256)
    
    # Cache configuration
    CACHE_TIMEOUT = timedelta(hours=1)
    
    # CORS configuration
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
    
    @staticmethod
    def init_app(app):
        # Create necessary directories
        directories = [
            Config.UPLOAD_FOLDER,
            Config.GENERATED_FOLDER,
            Config.CELEBRITY_DB_FOLDER
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}