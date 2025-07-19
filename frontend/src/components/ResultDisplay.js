import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Download, Share2, Heart, CheckCircle } from 'lucide-react';

const ResultDisplay = ({ result }) => {
  const [isDownloading, setIsDownloading] = useState(false);
  const [isLiked, setIsLiked] = useState(false);

  const handleDownload = async () => {
    setIsDownloading(true);
    try {
      const response = await fetch(`/download/${result.filename}`);
      const blob = await response.blob();
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = result.filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Download failed:', error);
    } finally {
      setIsDownloading(false);
    }
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'AI Generated Image',
          text: 'Check out this AI-generated image I created!',
          url: window.location.href,
        });
      } catch (error) {
        console.log('Share cancelled or failed');
      }
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      // You could show a toast notification here
    }
  };

  const getResultTitle = () => {
    if (result.type === 'famous-person') {
      return 'Your Celebrity Lookalike';
    } else if (result.type === 'cartoon') {
      const styleNames = {
        cartoon: 'Classic Cartoon',
        anime: 'Anime Style',
        comic: 'Comic Book',
        sketch: 'Pencil Sketch'
      };
      return `${styleNames[result.style] || 'Cartoon'} Generated`;
    }
    return 'Generated Image';
  };

  const getResultDescription = () => {
    if (result.type === 'famous-person') {
      return 'AI found a celebrity who looks similar to you!';
    } else if (result.type === 'cartoon') {
      return 'Your photo has been transformed into a beautiful cartoon character.';
    }
    return 'Your AI-generated image is ready!';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <div className="flex items-center justify-center space-x-2 mb-2">
          <CheckCircle className="h-6 w-6 text-green-500" />
          <h3 className="text-xl font-semibold text-green-700">Generation Complete!</h3>
        </div>
        <h4 className="text-lg font-medium mb-2">{getResultTitle()}</h4>
        <p className="text-gray-600">{getResultDescription()}</p>
      </div>

      {/* Generated Image */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="relative overflow-hidden rounded-lg bg-gray-100"
      >
        <img
          src={`/download/${result.filename}`}
          alt="Generated result"
          className="w-full h-auto max-h-96 object-contain"
        />
        
        {/* Image overlay with actions */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300">
          <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between">
            <div className="text-white">
              <p className="font-medium">{result.filename}</p>
              <p className="text-sm opacity-90">AI Generated</p>
            </div>
            <div className="flex space-x-2">
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setIsLiked(!isLiked)}
                className={`p-2 rounded-full ${
                  isLiked ? 'bg-red-500 text-white' : 'bg-white/20 text-white hover:bg-white/30'
                } transition-colors duration-200`}
              >
                <Heart className={`h-4 w-4 ${isLiked ? 'fill-current' : ''}`} />
              </motion.button>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-3">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleDownload}
          disabled={isDownloading}
          className="flex-1 btn-primary flex items-center justify-center space-x-2 disabled:opacity-50"
        >
          {isDownloading ? (
            <div className="loading-spinner h-4 w-4"></div>
          ) : (
            <Download className="h-4 w-4" />
          )}
          <span>{isDownloading ? 'Downloading...' : 'Download Image'}</span>
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleShare}
          className="flex-1 btn-secondary flex items-center justify-center space-x-2"
        >
          <Share2 className="h-4 w-4" />
          <span>Share</span>
        </motion.button>
      </div>

      {/* Result Info */}
      <div className="bg-gray-50 rounded-lg p-4">
        <h5 className="font-medium text-gray-900 mb-2">Generation Details</h5>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Type:</span>
            <p className="font-medium capitalize">
              {result.type === 'famous-person' ? 'Celebrity Match' : 'Cartoon Generation'}
            </p>
          </div>
          {result.style && (
            <div>
              <span className="text-gray-600">Style:</span>
              <p className="font-medium capitalize">{result.style}</p>
            </div>
          )}
          <div>
            <span className="text-gray-600">Status:</span>
            <p className="font-medium text-green-600">Success</p>
          </div>
          <div>
            <span className="text-gray-600">File:</span>
            <p className="font-medium truncate">{result.filename}</p>
          </div>
        </div>
      </div>

      {/* Success Message */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-green-50 border border-green-200 rounded-lg p-4"
      >
        <div className="flex items-center space-x-2">
          <CheckCircle className="h-5 w-5 text-green-600" />
          <p className="text-green-800 font-medium">Generation successful!</p>
        </div>
        <p className="text-green-700 text-sm mt-1">
          Your image has been processed and is ready for download. Feel free to generate more variations!
        </p>
      </motion.div>
    </div>
  );
};

export default ResultDisplay;