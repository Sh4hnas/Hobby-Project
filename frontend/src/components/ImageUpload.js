import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { Upload, Image, AlertCircle } from 'lucide-react';
import axios from 'axios';

const ImageUpload = ({ onImageUpload }) => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setUploading(true);
    setError(null);

    try {
      // Create FormData
      const formData = new FormData();
      formData.append('file', file);

      // Upload to backend
      const response = await axios.post('/upload-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Call parent callback with file and filename
      onImageUpload(file, response.data.filename);
    } catch (err) {
      console.error('Upload error:', err);
      setError(
        err.response?.data?.detail || 
        err.message || 
        'Failed to upload image. Please try again.'
      );
    } finally {
      setUploading(false);
    }
  }, [onImageUpload]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.bmp', '.tiff']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={`dropzone ${
          isDragActive ? 'dropzone-active' : ''
        } ${isDragReject ? 'border-red-400 bg-red-50' : ''}`}
      >
        <input {...getInputProps()} />
        
        {uploading ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-4"
          >
            <div className="loading-spinner mx-auto"></div>
            <p className="text-gray-600">Uploading your image...</p>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-4"
          >
            {isDragReject ? (
              <AlertCircle className="h-12 w-12 text-red-400 mx-auto" />
            ) : (
              <Upload className="h-12 w-12 text-primary-400 mx-auto" />
            )}
            
            <div>
              {isDragReject ? (
                <p className="text-red-600 font-medium">
                  Invalid file type. Please upload an image.
                </p>
              ) : isDragActive ? (
                <p className="text-primary-600 font-medium">
                  Drop your image here...
                </p>
              ) : (
                <div className="space-y-2">
                  <p className="text-gray-600 font-medium">
                    Drag & drop your image here, or click to browse
                  </p>
                  <p className="text-sm text-gray-500">
                    Supports: JPG, PNG, BMP, TIFF (Max 10MB)
                  </p>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center space-x-2 p-3 bg-red-50 border border-red-200 rounded-lg"
        >
          <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0" />
          <p className="text-red-700 text-sm">{error}</p>
        </motion.div>
      )}

      {/* Tips */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-medium text-blue-900 mb-2">Tips for best results:</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Use a clear, high-quality photo with good lighting</li>
          <li>• Make sure the face is clearly visible and facing forward</li>
          <li>• Avoid photos with multiple faces or heavily obscured features</li>
          <li>• For cartoon generation, simple backgrounds work best</li>
        </ul>
      </div>
    </div>
  );
};

export default ImageUpload;