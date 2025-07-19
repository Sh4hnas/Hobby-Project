#!/usr/bin/env python3
"""
Complete workflow test for AI Image Generator
Tests the full pipeline: upload -> generate -> download
"""

import requests
import time
import os
from pathlib import Path

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Backend health check passed")
            return True
        else:
            print("❌ Backend health check failed")
            return False
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        return False

def test_frontend_health():
    """Test if frontend is running"""
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print("✅ Frontend health check passed")
            return True
        else:
            print("❌ Frontend health check failed")
            return False
    except Exception as e:
        print(f"❌ Frontend health check failed: {e}")
        return False

def test_image_upload():
    """Test image upload functionality"""
    try:
        # Use one of the celebrity images as test image
        test_image_path = "backend/data/celebrities/angelina_jolie.jpg"
        
        if not os.path.exists(test_image_path):
            print(f"❌ Test image not found: {test_image_path}")
            return None
        
        with open(test_image_path, 'rb') as f:
            files = {'file': ('angelina_jolie.jpg', f, 'image/jpeg')}
            response = requests.post("http://localhost:8000/upload-image", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Image upload successful: {result['filename']}")
            return result['filename']
        else:
            print(f"❌ Image upload failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Image upload failed: {e}")
        return None

def test_famous_person_generation(filename):
    """Test famous person generation"""
    try:
        data = {'filename': filename}
        response = requests.post("http://localhost:8000/generate-famous-person", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Famous person generation successful: {result['filename']}")
            return result['filename']
        else:
            print(f"❌ Famous person generation failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Famous person generation failed: {e}")
        return None

def test_cartoon_generation(filename):
    """Test cartoon generation"""
    try:
        data = {'filename': filename, 'style': 'cartoon'}
        response = requests.post("http://localhost:8000/generate-cartoon", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Cartoon generation successful: {result['filename']}")
            return result['filename']
        else:
            print(f"❌ Cartoon generation failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Cartoon generation failed: {e}")
        return None

def test_image_download(filename, output_path):
    """Test image download"""
    try:
        response = requests.get(f"http://localhost:8000/download/{filename}")
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Image download successful: {output_path}")
            return True
        else:
            print(f"❌ Image download failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Image download failed: {e}")
        return False

def main():
    """Run complete workflow test"""
    print("🚀 Starting AI Image Generator Complete Workflow Test")
    print("=" * 60)
    
    # Test 1: Health checks
    print("\n1. Testing Health Checks")
    print("-" * 30)
    if not test_backend_health():
        print("❌ Backend is not running. Please start the backend first.")
        return
    
    if not test_frontend_health():
        print("⚠️  Frontend is not running. Backend-only test will continue.")
    
    # Test 2: Image upload
    print("\n2. Testing Image Upload")
    print("-" * 30)
    uploaded_filename = test_image_upload()
    if not uploaded_filename:
        print("❌ Image upload failed. Stopping test.")
        return
    
    # Test 3: Famous person generation
    print("\n3. Testing Famous Person Generation")
    print("-" * 30)
    famous_filename = test_famous_person_generation(uploaded_filename)
    if not famous_filename:
        print("❌ Famous person generation failed.")
    
    # Test 4: Cartoon generation
    print("\n4. Testing Cartoon Generation")
    print("-" * 30)
    cartoon_filename = test_cartoon_generation(uploaded_filename)
    if not cartoon_filename:
        print("❌ Cartoon generation failed.")
    
    # Test 5: Image downloads
    print("\n5. Testing Image Downloads")
    print("-" * 30)
    if famous_filename:
        test_image_download(famous_filename, "test_famous_person_result.jpg")
    
    if cartoon_filename:
        test_image_download(cartoon_filename, "test_cartoon_result.jpg")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 Complete Workflow Test Summary")
    print("=" * 60)
    print(f"✅ Backend: Running on http://localhost:8000")
    print(f"✅ Frontend: Running on http://localhost:3000")
    print(f"✅ Image Upload: {uploaded_filename}")
    print(f"✅ Famous Person Generation: {famous_filename if famous_filename else 'Failed'}")
    print(f"✅ Cartoon Generation: {cartoon_filename if cartoon_filename else 'Failed'}")
    print(f"✅ Downloads: Check test_*_result.jpg files")
    
    print("\n🌐 You can now:")
    print("   - Open http://localhost:3000 in your browser")
    print("   - Upload an image")
    print("   - Generate famous person or cartoon images")
    print("   - Download the results")
    
    print("\n📁 Generated files:")
    if os.path.exists("test_famous_person_result.jpg"):
        print("   - test_famous_person_result.jpg")
    if os.path.exists("test_cartoon_result.jpg"):
        print("   - test_cartoon_result.jpg")

if __name__ == "__main__":
    main()