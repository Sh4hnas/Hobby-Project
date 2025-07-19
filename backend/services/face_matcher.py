import insightface
from insightface.app import FaceAnalysis
import cv2
import numpy as np
import os
import requests
from pathlib import Path
import uuid
from typing import List, Tuple, Optional
import json

class FaceMatcher:
    def __init__(self):
        """
        Initialize the face matching service with InsightFace
        """
        self.app = FaceAnalysis(name='buffalo_l')
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        
        # Famous people database (you can expand this)
        self.famous_people_db = {
            "actors": [
                {"name": "Tom Hanks", "image_url": "https://example.com/tom_hanks.jpg"},
                {"name": "Brad Pitt", "image_url": "https://example.com/brad_pitt.jpg"},
                {"name": "Angelina Jolie", "image_url": "https://example.com/angelina_jolie.jpg"},
                {"name": "Leonardo DiCaprio", "image_url": "https://example.com/leonardo_dicaprio.jpg"},
                {"name": "Scarlett Johansson", "image_url": "https://example.com/scarlett_johansson.jpg"},
            ],
            "musicians": [
                {"name": "Taylor Swift", "image_url": "https://example.com/taylor_swift.jpg"},
                {"name": "Ed Sheeran", "image_url": "https://example.com/ed_sheeran.jpg"},
                {"name": "Beyoncé", "image_url": "https://example.com/beyonce.jpg"},
                {"name": "Justin Bieber", "image_url": "https://example.com/justin_bieber.jpg"},
            ],
            "athletes": [
                {"name": "Cristiano Ronaldo", "image_url": "https://example.com/ronaldo.jpg"},
                {"name": "Lionel Messi", "image_url": "https://example.com/messi.jpg"},
                {"name": "Serena Williams", "image_url": "https://example.com/serena_williams.jpg"},
            ]
        }
        
        # Cache for celebrity embeddings
        self.celebrity_embeddings = {}
        self.celebrity_images = {}
        
        # Load celebrity database
        self._load_celebrity_database()
    
    def _load_celebrity_database(self):
        """
        Load celebrity images and compute embeddings
        """
        celebrity_dir = Path("data/celebrities")
        celebrity_dir.mkdir(parents=True, exist_ok=True)
        
        # For now, we'll use placeholder images
        # In a real implementation, you would download and store celebrity images
        self._create_placeholder_celebrities()
    
    def _create_placeholder_celebrities(self):
        """
        Create placeholder celebrity images for demonstration
        """
        celebrity_dir = Path("data/celebrities")
        
        # Create some placeholder celebrity images
        celebrities = [
            "tom_hanks", "brad_pitt", "angelina_jolie", 
            "leonardo_dicaprio", "scarlett_johansson",
            "taylor_swift", "ed_sheeran", "beyonce"
        ]
        
        for celeb in celebrities:
            celeb_path = celebrity_dir / f"{celeb}.jpg"
            if not celeb_path.exists():
                # Create a simple placeholder image
                placeholder = np.ones((224, 224, 3), dtype=np.uint8) * 128
                cv2.imwrite(str(celeb_path), placeholder)
    
    def extract_face_embedding(self, image_path: str) -> Optional[np.ndarray]:
        """
        Extract face embedding from an image
        """
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                return None
            
            # Convert BGR to RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            faces = self.app.get(img_rgb)
            
            if len(faces) == 0:
                return None
            
            # Get embedding of the first face
            embedding = faces[0].embedding
            return embedding
            
        except Exception as e:
            print(f"Error extracting face embedding: {e}")
            return None
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two face embeddings
        """
        # Normalize embeddings
        emb1_norm = embedding1 / np.linalg.norm(embedding1)
        emb2_norm = embedding2 / np.linalg.norm(embedding2)
        
        # Compute cosine similarity
        similarity = np.dot(emb1_norm, emb2_norm)
        return float(similarity)
    
    def find_most_similar_celebrity(self, user_embedding: np.ndarray) -> Tuple[str, float, str]:
        """
        Find the most similar celebrity to the user's face
        """
        best_match = None
        best_similarity = -1
        best_image_path = None
        
        celebrity_dir = Path("data/celebrities")
        
        for celeb_file in celebrity_dir.glob("*.jpg"):
            try:
                # Extract celebrity embedding
                celeb_embedding = self.extract_face_embedding(str(celeb_file))
                
                if celeb_embedding is not None:
                    # Compute similarity
                    similarity = self.compute_similarity(user_embedding, celeb_embedding)
                    
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match = celeb_file.stem
                        best_image_path = str(celeb_file)
                        
            except Exception as e:
                print(f"Error processing celebrity {celeb_file}: {e}")
                continue
        
        return best_match, best_similarity, best_image_path
    
    async def find_similar_famous_person(self, image_path: str) -> str:
        """
        Find a famous person similar to the uploaded image
        """
        # Extract face embedding from user image
        user_embedding = self.extract_face_embedding(image_path)
        
        if user_embedding is None:
            raise ValueError("No face detected in the uploaded image")
        
        # Find most similar celebrity
        celebrity_name, similarity, celebrity_image_path = self.find_most_similar_celebrity(user_embedding)
        
        if celebrity_name is None:
            raise ValueError("No suitable celebrity match found")
        
        # For now, return the celebrity image directly
        # In a more advanced implementation, you could use face swapping
        output_filename = f"famous_person_{uuid.uuid4()}.jpg"
        output_path = Path("generated") / output_filename
        
        # Copy celebrity image to output
        import shutil
        shutil.copy2(celebrity_image_path, output_path)
        
        return str(output_path)
    
    def get_celebrity_info(self, celebrity_name: str) -> dict:
        """
        Get information about a celebrity
        """
        # This would typically query a database
        return {
            "name": celebrity_name.replace("_", " ").title(),
            "category": "Actor",  # This would be determined from the database
            "similarity_score": 0.85  # This would be the actual similarity score
        }