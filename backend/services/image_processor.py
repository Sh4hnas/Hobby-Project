import cv2
import numpy as np
from PIL import Image
import os
from pathlib import Path
from typing import Tuple, Optional

class ImageProcessor:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def load_image(self, image_path: str) -> np.ndarray:
        """
        Load an image from path
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")
        
        return image
    
    def save_image(self, image: np.ndarray, output_path: str) -> str:
        """
        Save an image to path
        """
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        success = cv2.imwrite(output_path, image)
        if not success:
            raise ValueError(f"Failed to save image: {output_path}")
        
        return output_path
    
    def resize_image(self, image: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
        """
        Resize image to target size
        """
        return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
    
    def detect_faces(self, image: np.ndarray) -> list:
        """
        Detect faces in the image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        return faces
    
    def extract_face_region(self, image: np.ndarray, face_coords: Tuple[int, int, int, int]) -> np.ndarray:
        """
        Extract face region from image
        """
        x, y, w, h = face_coords
        face_region = image[y:y+h, x:x+w]
        return face_region
    
    def preprocess_for_ai(self, image: np.ndarray, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
        """
        Preprocess image for AI model input
        """
        # Resize to target size
        resized = self.resize_image(image, target_size)
        
        # Normalize pixel values
        normalized = resized.astype(np.float32) / 255.0
        
        return normalized
    
    def convert_to_pil(self, image: np.ndarray) -> Image.Image:
        """
        Convert OpenCV image to PIL Image
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_image)
    
    def convert_from_pil(self, pil_image: Image.Image) -> np.ndarray:
        """
        Convert PIL Image to OpenCV format
        """
        # Convert to numpy array
        np_image = np.array(pil_image)
        
        # Convert RGB to BGR
        bgr_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
        return bgr_image
    
    def validate_image(self, image_path: str) -> bool:
        """
        Validate if the image is suitable for processing
        """
        try:
            image = self.load_image(image_path)
            
            # Check if image is not empty
            if image.size == 0:
                return False
            
            # Check minimum size
            height, width = image.shape[:2]
            if height < 100 or width < 100:
                return False
            
            # Check if face is detected
            faces = self.detect_faces(image)
            if len(faces) == 0:
                return False
            
            return True
            
        except Exception as e:
            print(f"Image validation failed: {e}")
            return False