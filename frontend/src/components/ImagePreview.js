import React from 'react';
import { motion } from 'framer-motion';

const ImagePreview = ({ image }) => {
  const imageUrl = URL.createObjectURL(image);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      className="relative"
    >
      <div className="relative overflow-hidden rounded-lg bg-gray-100">
        <img
          src={imageUrl}
          alt="Uploaded preview"
          className="w-full h-auto max-h-96 object-contain"
          onLoad={() => {
            // Clean up the object URL when image loads
            // URL.revokeObjectURL(imageUrl);
          }}
        />
        
        {/* Image info overlay */}
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4">
          <div className="text-white text-sm">
            <p className="font-medium">{image.name}</p>
            <p className="opacity-90">
              {(image.size / 1024 / 1024).toFixed(2)} MB • {image.type}
            </p>
          </div>
        </div>
      </div>
      
      {/* Image details */}
      <div className="mt-3 grid grid-cols-2 gap-4 text-sm text-gray-600">
        <div>
          <span className="font-medium">File name:</span>
          <p className="truncate">{image.name}</p>
        </div>
        <div>
          <span className="font-medium">Size:</span>
          <p>{(image.size / 1024 / 1024).toFixed(2)} MB</p>
        </div>
      </div>
    </motion.div>
  );
};

export default ImagePreview;