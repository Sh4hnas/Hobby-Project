from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import io
import numpy as np
from PIL import Image
import cv2
import json
import requests
from datetime import datetime
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated'
CELEBRITY_DB_FOLDER = 'celebrity_db'

# Create directories if they don't exist
for folder in [UPLOAD_FOLDER, GENERATED_FOLDER, CELEBRITY_DB_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Celebrity database (in production, this would be a proper database)
CELEBRITIES = {
    "actors": [
        {"name": "Robert Downey Jr.", "image": "rdj.jpg", "description": "Iron Man actor"},
        {"name": "Scarlett Johansson", "image": "scarlett.jpg", "description": "Black Widow actress"},
        {"name": "Chris Evans", "image": "chris_evans.jpg", "description": "Captain America actor"},
        {"name": "Emma Stone", "image": "emma_stone.jpg", "description": "La La Land actress"},
        {"name": "Ryan Reynolds", "image": "ryan_reynolds.jpg", "description": "Deadpool actor"}
    ],
    "cartoons": [
        {"name": "Mickey Mouse", "image": "mickey.jpg", "description": "Disney's iconic mouse"},
        {"name": "Superman", "image": "superman.jpg", "description": "DC's Man of Steel"},
        {"name": "Batman", "image": "batman.jpg", "description": "DC's Dark Knight"},
        {"name": "Wonder Woman", "image": "wonder_woman.jpg", "description": "DC's Amazon warrior"},
        {"name": "Spider-Man", "image": "spiderman.jpg", "description": "Marvel's web-slinger"}
    ]
}

class SimpleFaceMatcher:
    def __init__(self):
        pass
    
    def find_similar_celebrities(self, user_image_path, threshold=0.6):
        """Find celebrities similar to the user's face (simplified version)"""
        # For demo purposes, return random celebrities with random similarity scores
        # In production, you'd use actual face recognition
        all_celebrities = CELEBRITIES["actors"] + CELEBRITIES["cartoons"]
        selected = random.sample(all_celebrities, min(3, len(all_celebrities)))
        
        for celebrity in selected:
            celebrity["similarity_score"] = random.uniform(0.7, 0.95)
        
        return sorted(selected, key=lambda x: x["similarity_score"], reverse=True)

class SimpleImageGenerator:
    def __init__(self):
        pass
        
    def generate_celebrity_style(self, user_image_path, celebrity_name, style="realistic"):
        """Generate an image in celebrity style (simplified version)"""
        try:
            # Load user image
            user_image = Image.open(user_image_path)
            
            # Apply style transfer (simplified)
            processed_image = self.apply_style_transfer(user_image, celebrity_name, style)
            
            # Save generated image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = celebrity_name.replace(" ", "_").replace(".", "")
            output_path = os.path.join(GENERATED_FOLDER, f"generated_{safe_name}_{timestamp}.jpg")
            processed_image.save(output_path)
            
            return output_path
        except Exception as e:
            logger.error(f"Error generating celebrity style image: {e}")
            return None
    
    def apply_style_transfer(self, image, celebrity_name, style):
        """Apply style transfer to make image look like celebrity/cartoon"""
        # Convert PIL to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Apply some basic image processing as a placeholder
        if style == "cartoon":
            # Cartoon-like effect
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            gray_blur = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(cv_image, 9, 300, 300)
            cartoon = cv2.bitwise_and(color, color, mask=edges)
            cv_image = cartoon
        else:
            # Apply some filters for "celebrity" style
            cv_image = cv2.bilateralFilter(cv_image, 15, 80, 80)
            # Add slight color adjustment
            cv_image = cv2.convertScaleAbs(cv_image, alpha=1.1, beta=10)
        
        # Convert back to PIL
        result_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        return result_image

# Initialize AI components
face_matcher = SimpleFaceMatcher()
image_generator = SimpleImageGenerator()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "AI Celebrity Generator API is running"})

@app.route('/api/upload', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"user_upload_{timestamp}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Find similar celebrities
        similar_celebrities = face_matcher.find_similar_celebrities(filepath)
        
        return jsonify({
            "success": True,
            "upload_id": timestamp,
            "similar_celebrities": similar_celebrities,
            "message": "Image uploaded and analyzed successfully"
        })
    
    except Exception as e:
        logger.error(f"Error in upload_image: {e}")
        return jsonify({"error": "Failed to process image"}), 500

@app.route('/api/generate', methods=['POST'])
def generate_image():
    try:
        data = request.json
        upload_id = data.get('upload_id')
        celebrity_name = data.get('celebrity_name')
        style = data.get('style', 'realistic')
        
        if not upload_id or not celebrity_name:
            return jsonify({"error": "Missing required parameters"}), 400
        
        # Find the uploaded image
        user_image_path = None
        for filename in os.listdir(UPLOAD_FOLDER):
            if upload_id in filename:
                user_image_path = os.path.join(UPLOAD_FOLDER, filename)
                break
        
        if not user_image_path:
            return jsonify({"error": "Original image not found"}), 404
        
        # Generate celebrity-style image
        generated_image_path = image_generator.generate_celebrity_style(
            user_image_path, celebrity_name, style
        )
        
        if not generated_image_path:
            return jsonify({"error": "Failed to generate image"}), 500
        
        return jsonify({
            "success": True,
            "generated_image": os.path.basename(generated_image_path),
            "message": f"Generated {style} style image similar to {celebrity_name}"
        })
    
    except Exception as e:
        logger.error(f"Error in generate_image: {e}")
        return jsonify({"error": "Failed to generate image"}), 500

@app.route('/api/image/<filename>')
def get_generated_image(filename):
    try:
        return send_file(os.path.join(GENERATED_FOLDER, filename))
    except Exception as e:
        logger.error(f"Error serving image: {e}")
        return jsonify({"error": "Image not found"}), 404

@app.route('/api/celebrities')
def get_celebrities():
    return jsonify(CELEBRITIES)

if __name__ == '__main__':
    print("🚀 Starting AI Celebrity Generator API...")
    print("📍 Server will be available at: http://localhost:5000")
    print("💡 Make sure to install required dependencies: pip install -r requirements_simple.txt")
    print("🎯 API endpoints:")
    print("   - GET  /api/health - Health check")
    print("   - POST /api/upload - Upload and analyze photo")
    print("   - POST /api/generate - Generate celebrity-style image")
    print("   - GET  /api/image/<filename> - Get generated images")
    print("   - GET  /api/celebrities - Get celebrity database")
    app.run(debug=True, host='0.0.0.0', port=5000)