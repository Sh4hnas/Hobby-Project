from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
import uuid
from datetime import datetime
from pathlib import Path

from config import UPLOAD_DIR, GENERATED_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from services.image_processor import ImageProcessor
from services.face_matcher import FaceMatcher
from services.cartoon_generator import CartoonGenerator

app = FastAPI(title="AI Image Generator", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
image_processor = ImageProcessor()
face_matcher = FaceMatcher()
cartoon_generator = CartoonGenerator()

@app.get("/")
async def root():
    return {"message": "AI Image Generator API", "status": "running"}

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image for processing
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Validate file extension
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"File extension not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save uploaded file
    try:
        content = await file.read()
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
            
        # Validate the uploaded image
        if not image_processor.validate_image(str(file_path)):
            # Delete the file if validation fails
            file_path.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail="No face detected in image or image is invalid")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    return {
        "message": "Image uploaded successfully",
        "filename": unique_filename,
        "file_path": str(file_path)
    }

@app.post("/generate-famous-person")
async def generate_famous_person(filename: str = Form(...)):
    """
    Generate an image of a famous person similar to the uploaded image
    """
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        # Process the image and find similar famous person
        result_path = await face_matcher.find_similar_famous_person(str(file_path))
        
        return {
            "message": "Famous person image generated successfully",
            "result_path": result_path,
            "filename": Path(result_path).name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate image: {str(e)}")

@app.post("/generate-cartoon")
async def generate_cartoon(filename: str = Form(...), style: str = Form("cartoon")):
    """
    Generate a cartoon character similar to the uploaded image
    """
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        # Process the image and generate cartoon
        result_path = await cartoon_generator.generate_cartoon(str(file_path), style)
        
        return {
            "message": "Cartoon image generated successfully",
            "result_path": result_path,
            "filename": Path(result_path).name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate cartoon: {str(e)}")

@app.get("/download/{filename}")
async def download_image(filename: str):
    """
    Download a generated image
    """
    file_path = GENERATED_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="image/jpeg"
    )

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    from config import API_HOST, API_PORT, DEBUG
    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=DEBUG)