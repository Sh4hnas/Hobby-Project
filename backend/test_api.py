#!/usr/bin/env python3
"""
Test script for the AI Image Generator API
"""

import requests
import time
import os
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running.")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint passed: {data}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def create_test_image():
    """Create a simple test image"""
    import numpy as np
    import cv2
    
    # Create a simple test image with a face-like pattern
    img = np.ones((300, 300, 3), dtype=np.uint8) * 200
    
    # Draw a simple face
    cv2.circle(img, (150, 100), 50, (255, 200, 150), -1)  # Head
    cv2.circle(img, (130, 90), 5, (0, 0, 0), -1)  # Left eye
    cv2.circle(img, (170, 90), 5, (0, 0, 0), -1)  # Right eye
    cv2.ellipse(img, (150, 120), (20, 10), 0, 0, 180, (0, 0, 0), 2)  # Mouth
    
    # Save the test image
    test_image_path = "test_image.jpg"
    cv2.imwrite(test_image_path, img)
    return test_image_path

def test_upload_image(image_path):
    """Test image upload"""
    print("Testing image upload...")
    try:
        with open(image_path, 'rb') as f:
            files = {'file': ('test_image.jpg', f, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/upload-image", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Image upload passed: {data['filename']}")
            return data['filename']
        else:
            print(f"❌ Image upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Image upload error: {e}")
        return None

def test_generate_cartoon(filename):
    """Test cartoon generation"""
    print("Testing cartoon generation...")
    try:
        data = {'filename': filename, 'style': 'cartoon'}
        response = requests.post(f"{BASE_URL}/generate-cartoon", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Cartoon generation passed: {result['filename']}")
            return result['filename']
        else:
            print(f"❌ Cartoon generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Cartoon generation error: {e}")
        return None

def test_generate_famous_person(filename):
    """Test famous person generation"""
    print("Testing famous person generation...")
    try:
        data = {'filename': filename}
        response = requests.post(f"{BASE_URL}/generate-famous-person", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Famous person generation passed: {result['filename']}")
            return result['filename']
        else:
            print(f"❌ Famous person generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Famous person generation error: {e}")
        return None

def test_download_image(filename):
    """Test image download"""
    print("Testing image download...")
    try:
        response = requests.get(f"{BASE_URL}/download/{filename}")
        
        if response.status_code == 200:
            # Save the downloaded image
            output_path = f"downloaded_{filename}"
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Image download passed: {output_path}")
            return True
        else:
            print(f"❌ Image download failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Image download error: {e}")
        return False

def cleanup():
    """Clean up test files"""
    print("Cleaning up test files...")
    files_to_remove = [
        "test_image.jpg",
        "downloaded_cartoon_*.jpg",
        "downloaded_famous_person_*.jpg"
    ]
    
    for pattern in files_to_remove:
        for file_path in Path(".").glob(pattern):
            try:
                file_path.unlink()
                print(f"Removed: {file_path}")
            except Exception as e:
                print(f"Could not remove {file_path}: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting API tests...")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health_check():
        print("❌ Health check failed. Stopping tests.")
        return
    
    # Test 2: Root endpoint
    if not test_root_endpoint():
        print("❌ Root endpoint failed. Stopping tests.")
        return
    
    # Test 3: Create test image
    print("Creating test image...")
    test_image_path = create_test_image()
    print(f"✅ Test image created: {test_image_path}")
    
    # Test 4: Upload image
    uploaded_filename = test_upload_image(test_image_path)
    if not uploaded_filename:
        print("❌ Image upload failed. Stopping tests.")
        return
    
    # Test 5: Generate cartoon
    cartoon_filename = test_generate_cartoon(uploaded_filename)
    if cartoon_filename:
        test_download_image(cartoon_filename)
    
    # Test 6: Generate famous person
    famous_filename = test_generate_famous_person(uploaded_filename)
    if famous_filename:
        test_download_image(famous_filename)
    
    # Cleanup
    cleanup()
    
    print("=" * 50)
    print("🎉 API tests completed!")

if __name__ == "__main__":
    main()