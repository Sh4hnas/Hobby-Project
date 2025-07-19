import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, Sparkles, Download, RefreshCw } from 'lucide-react';
import ImageUpload from '../components/ImageUpload';
import ImagePreview from '../components/ImagePreview';
import GenerationOptions from '../components/GenerationOptions';
import ResultDisplay from '../components/ResultDisplay';
import { generateFamousPerson, generateCartoon } from '../services/api';

const Home = () => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [uploadedFilename, setUploadedFilename] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleImageUpload = (file, filename) => {
    setUploadedImage(file);
    setUploadedFilename(filename);
    setResult(null);
    setError(null);
  };

  const handleGenerate = async (type, options = {}) => {
    if (!uploadedFilename) {
      setError('Please upload an image first');
      return;
    }

    setIsProcessing(true);
    setError(null);
    setResult(null);

    try {
      let response;
      if (type === 'famous-person') {
        response = await generateFamousPerson(uploadedFilename);
      } else if (type === 'cartoon') {
        response = await generateCartoon(uploadedFilename, options.style);
      }

      setResult({
        type,
        filename: response.filename,
        message: response.message,
        ...options
      });
    } catch (err) {
      setError(err.message || 'An error occurred during generation');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReset = () => {
    setUploadedImage(null);
    setUploadedFilename(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center mb-12"
      >
        <h1 className="text-4xl md:text-6xl font-bold mb-6">
          <span className="gradient-text">AI Image Generator</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Upload your photo and watch AI transform it into a famous person lookalike 
          or a stunning cartoon character. Powered by advanced face recognition technology.
        </p>
        <div className="flex items-center justify-center space-x-4 text-sm text-gray-500">
          <div className="flex items-center space-x-2">
            <Sparkles className="h-4 w-4 text-primary-600" />
            <span>AI-Powered</span>
          </div>
          <div className="flex items-center space-x-2">
            <Upload className="h-4 w-4 text-primary-600" />
            <span>Easy Upload</span>
          </div>
          <div className="flex items-center space-x-2">
            <Download className="h-4 w-4 text-primary-600" />
            <span>Instant Download</span>
          </div>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column - Upload and Preview */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="space-y-6"
        >
          {/* Image Upload */}
          <div className="card">
            <h2 className="text-2xl font-semibold mb-4 flex items-center space-x-2">
              <Upload className="h-6 w-6 text-primary-600" />
              <span>Upload Your Photo</span>
            </h2>
            <ImageUpload onImageUpload={handleImageUpload} />
          </div>

          {/* Image Preview */}
          {uploadedImage && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
              className="card"
            >
              <h3 className="text-lg font-semibold mb-4">Your Photo</h3>
              <ImagePreview image={uploadedImage} />
              <button
                onClick={handleReset}
                className="mt-4 btn-secondary flex items-center space-x-2"
              >
                <RefreshCw className="h-4 w-4" />
                <span>Upload New Photo</span>
              </button>
            </motion.div>
          )}
        </motion.div>

        {/* Right Column - Generation Options and Results */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="space-y-6"
        >
          {/* Generation Options */}
          {uploadedImage && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="card"
            >
              <h2 className="text-2xl font-semibold mb-4 flex items-center space-x-2">
                <Sparkles className="h-6 w-6 text-primary-600" />
                <span>Choose Your Style</span>
              </h2>
              <GenerationOptions
                onGenerate={handleGenerate}
                isProcessing={isProcessing}
              />
            </motion.div>
          )}

          {/* Processing State */}
          {isProcessing && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="card text-center"
            >
              <div className="loading-spinner mx-auto mb-4"></div>
              <h3 className="text-lg font-semibold mb-2">Processing Your Image</h3>
              <p className="text-gray-600">
                Our AI is working its magic... This may take a few moments.
              </p>
            </motion.div>
          )}

          {/* Error Display */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="card bg-red-50 border-red-200"
            >
              <h3 className="text-lg font-semibold text-red-800 mb-2">Error</h3>
              <p className="text-red-600">{error}</p>
            </motion.div>
          )}

          {/* Results Display */}
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="card"
            >
              <ResultDisplay result={result} />
            </motion.div>
          )}
        </motion.div>
      </div>

      {/* Features Section */}
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.6 }}
        className="mt-16"
      >
        <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Upload className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">1. Upload Photo</h3>
            <p className="text-gray-600">
              Simply drag and drop or click to upload a clear photo with a visible face.
            </p>
          </div>
          <div className="text-center">
            <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Sparkles className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">2. Choose Style</h3>
            <p className="text-gray-600">
              Select between famous person matching or various cartoon styles.
            </p>
          </div>
          <div className="text-center">
            <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Download className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">3. Download Result</h3>
            <p className="text-gray-600">
              Get your AI-generated image instantly and download it in high quality.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Home;