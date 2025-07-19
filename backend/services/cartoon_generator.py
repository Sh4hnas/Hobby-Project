import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import os
from pathlib import Path
import uuid
from typing import Tuple

class CartoonGenerator:
    def __init__(self):
        """
        Initialize the cartoon generator service
        """
        self.cartoon_styles = {
            "anime": self._apply_anime_style,
            "comic": self._apply_comic_style,
            "cartoon": self._apply_cartoon_style,
            "sketch": self._apply_sketch_style
        }
    
    def _apply_anime_style(self, image: np.ndarray) -> np.ndarray:
        """
        Apply anime-style cartoon effect
        """
        # Convert to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Apply bilateral filter to smooth the image while preserving edges
        smooth = cv2.bilateralFilter(rgb_image, 9, 75, 75)
        
        # Apply median blur to reduce noise
        smooth = cv2.medianBlur(smooth, 7)
        
        # Convert back to BGR
        return cv2.cvtColor(smooth, cv2.COLOR_RGB2BGR)
    
    def _apply_comic_style(self, image: np.ndarray) -> np.ndarray:
        """
        Apply comic book style effect
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2
        )
        
        # Apply color quantization
        color = cv2.bilateralFilter(image, 9, 300, 300)
        
        # Combine edges with color
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        
        return cartoon
    
    def _apply_cartoon_style(self, image: np.ndarray) -> np.ndarray:
        """
        Apply classic cartoon effect
        """
        # Convert to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Apply bilateral filter
        smooth = cv2.bilateralFilter(rgb_image, 15, 80, 80)
        
        # Apply edge detection
        gray = cv2.cvtColor(smooth, cv2.COLOR_RGB2GRAY)
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Convert edges to 3-channel
        edges_3d = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        
        # Combine smooth image with edges
        cartoon = cv2.bitwise_and(smooth, edges_3d)
        
        # Convert back to BGR
        return cv2.cvtColor(cartoon, cv2.COLOR_RGB2BGR)
    
    def _apply_sketch_style(self, image: np.ndarray) -> np.ndarray:
        """
        Apply pencil sketch effect
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Invert the grayscale image
        inv = 255 - gray
        
        # Apply Gaussian blur
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        
        # Invert the blurred image
        inv_blur = 255 - blur
        
        # Create sketch effect
        sketch = cv2.divide(gray, inv_blur, scale=256.0)
        
        # Convert back to 3-channel
        sketch_3d = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
        
        return sketch_3d
    
    def _enhance_colors(self, image: np.ndarray, saturation_factor: float = 1.5) -> np.ndarray:
        """
        Enhance colors in the image
        """
        # Convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Increase saturation
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_factor, 0, 255)
        
        # Convert back to BGR
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    def _add_outline(self, image: np.ndarray, outline_color: Tuple[int, int, int] = (0, 0, 0), thickness: int = 2) -> np.ndarray:
        """
        Add outline to the image
        """
        # Create a copy of the image
        outlined = image.copy()
        
        # Get image dimensions
        height, width = image.shape[:2]
        
        # Add border
        outlined = cv2.copyMakeBorder(
            outlined, thickness, thickness, thickness, thickness,
            cv2.BORDER_CONSTANT, value=outline_color
        )
        
        return outlined
    
    def _apply_watercolor_effect(self, image: np.ndarray) -> np.ndarray:
        """
        Apply watercolor painting effect
        """
        # Convert to PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # Apply various filters
        # Blur slightly
        blurred = pil_image.filter(ImageFilter.GaussianBlur(radius=1))
        
        # Enhance colors
        enhancer = ImageEnhance.Color(blurred)
        enhanced = enhancer.enhance(1.3)
        
        # Enhance contrast
        contrast_enhancer = ImageEnhance.Contrast(enhanced)
        final = contrast_enhancer.enhance(1.2)
        
        # Convert back to OpenCV format
        return cv2.cvtColor(np.array(final), cv2.COLOR_RGB2BGR)
    
    async def generate_cartoon(self, image_path: str, style: str = "cartoon") -> str:
        """
        Generate a cartoon version of the uploaded image
        """
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")
        
        # Apply the selected cartoon style
        if style in self.cartoon_styles:
            cartoon_image = self.cartoon_styles[style](image)
        else:
            # Default to cartoon style
            cartoon_image = self.cartoon_styles["cartoon"](image)
        
        # Enhance colors
        cartoon_image = self._enhance_colors(cartoon_image)
        
        # Add outline for better cartoon effect
        cartoon_image = self._add_outline(cartoon_image)
        
        # Apply watercolor effect for more artistic look
        cartoon_image = self._apply_watercolor_effect(cartoon_image)
        
        # Save the result
        output_filename = f"cartoon_{uuid.uuid4()}.jpg"
        output_path = Path("generated") / output_filename
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the image
        success = cv2.imwrite(str(output_path), cartoon_image)
        if not success:
            raise ValueError(f"Failed to save cartoon image: {output_path}")
        
        return str(output_path)
    
    def get_available_styles(self) -> list:
        """
        Get list of available cartoon styles
        """
        return list(self.cartoon_styles.keys())
    
    def preview_style(self, image_path: str, style: str) -> np.ndarray:
        """
        Generate a preview of a specific cartoon style
        """
        if style not in self.cartoon_styles:
            raise ValueError(f"Unknown style: {style}")
        
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")
        
        # Apply the style
        return self.cartoon_styles[style](image)