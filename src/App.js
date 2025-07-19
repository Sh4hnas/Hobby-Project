import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './App.css';

const API_BASE_URL = process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:5000/api';

function App() {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [uploadId, setUploadId] = useState(null);
  const [similarCelebrities, setSimilarCelebrities] = useState([]);
  const [selectedCelebrity, setSelectedCelebrity] = useState(null);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(1); // 1: Upload, 2: Select Celebrity, 3: Results
  const [selectedStyle, setSelectedStyle] = useState('realistic');

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setLoading(true);
    setUploadedImage(URL.createObjectURL(file));

    try {
      const formData = new FormData();
      formData.append('image', file);

      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (response.data.success) {
        setUploadId(response.data.upload_id);
        setSimilarCelebrities(response.data.similar_celebrities);
        setStep(2);
      }
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Failed to upload image. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif']
    },
    multiple: false
  });

  const generateImage = async (celebrity, style) => {
    setLoading(true);
    setSelectedCelebrity(celebrity);
    setSelectedStyle(style);

    try {
      const response = await axios.post(`${API_BASE_URL}/generate`, {
        upload_id: uploadId,
        celebrity_name: celebrity.name,
        style: style
      });

      if (response.data.success) {
        setGeneratedImage(`${API_BASE_URL}/image/${response.data.generated_image}`);
        setStep(3);
      }
    } catch (error) {
      console.error('Generation failed:', error);
      alert('Failed to generate image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const resetApp = () => {
    setUploadedImage(null);
    setUploadId(null);
    setSimilarCelebrities([]);
    setSelectedCelebrity(null);
    setGeneratedImage(null);
    setStep(1);
    setSelectedStyle('realistic');
  };

  const CelebrityCard = ({ celebrity, onSelect }) => (
    <div className="celebrity-card glass-effect rounded-xl p-6 text-center text-white">
      <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-2xl font-bold">
        {celebrity.name.charAt(0)}
      </div>
      <h3 className="font-semibold mb-2">{celebrity.name}</h3>
      <p className="text-sm text-gray-300 mb-4">{celebrity.description}</p>
      <div className="text-sm text-yellow-300 mb-4">
        Similarity: {(celebrity.similarity_score * 100).toFixed(1)}%
      </div>
      <div className="space-y-2">
        <button
          onClick={() => onSelect(celebrity, 'realistic')}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors"
        >
          Realistic Style
        </button>
        <button
          onClick={() => onSelect(celebrity, 'cartoon')}
          className="w-full bg-purple-600 hover:bg-purple-700 text-white py-2 px-4 rounded-lg transition-colors"
        >
          Cartoon Style
        </button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-white mb-4">
            AI Celebrity Generator
          </h1>
          <p className="text-xl text-gray-200">
            Upload your photo and discover which celebrity or cartoon character you look like!
          </p>
        </div>

        {/* Step 1: Upload Image */}
        {step === 1 && (
          <div className="fade-in">
            <div className="glass-effect rounded-2xl p-8 mb-8">
              <div
                {...getRootProps()}
                className={`upload-area border-2 border-dashed border-white/30 rounded-xl p-12 text-center cursor-pointer ${
                  isDragActive ? 'border-blue-400 bg-blue-50/10' : ''
                }`}
              >
                <input {...getInputProps()} />
                <div className="text-6xl mb-4">📸</div>
                <h3 className="text-2xl font-semibold text-white mb-2">
                  {isDragActive ? 'Drop your photo here!' : 'Upload Your Photo'}
                </h3>
                <p className="text-gray-300">
                  Drag and drop an image here, or click to select a file
                </p>
                <p className="text-sm text-gray-400 mt-2">
                  Supports JPG, PNG, GIF files
                </p>
              </div>
            </div>

            {uploadedImage && (
              <div className="glass-effect rounded-2xl p-8 text-center">
                <img
                  src={uploadedImage}
                  alt="Uploaded"
                  className="max-w-md mx-auto rounded-lg shadow-lg mb-4"
                />
                {loading && (
                  <div className="flex items-center justify-center">
                    <div className="loading-spinner mr-3"></div>
                    <span className="text-white">Analyzing your photo...</span>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Step 2: Select Celebrity */}
        {step === 2 && (
          <div className="fade-in">
            <div className="glass-effect rounded-2xl p-8 mb-8">
              <h2 className="text-3xl font-bold text-white text-center mb-8">
                Choose Your Lookalike
              </h2>
              
              <div className="grid md:grid-cols-2 gap-8 mb-8">
                <div>
                  <h3 className="text-xl font-semibold text-white mb-4">Your Photo</h3>
                  <img
                    src={uploadedImage}
                    alt="Your upload"
                    className="w-full max-w-sm rounded-lg shadow-lg"
                  />
                </div>
                
                <div>
                  <h3 className="text-xl font-semibold text-white mb-4">Similar Celebrities</h3>
                  <div className="grid gap-4">
                    {similarCelebrities.map((celebrity, index) => (
                      <CelebrityCard
                        key={index}
                        celebrity={celebrity}
                        onSelect={generateImage}
                      />
                    ))}
                  </div>
                </div>
              </div>

              {loading && (
                <div className="text-center">
                  <div className="loading-spinner mx-auto mb-3"></div>
                  <p className="text-white">Generating your celebrity lookalike...</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Step 3: Results */}
        {step === 3 && (
          <div className="fade-in">
            <div className="glass-effect rounded-2xl p-8">
              <h2 className="text-3xl font-bold text-white text-center mb-8">
                Your Celebrity Transformation
              </h2>
              
              <div className="grid md:grid-cols-3 gap-8 mb-8">
                <div className="text-center">
                  <h3 className="text-xl font-semibold text-white mb-4">Original</h3>
                  <img
                    src={uploadedImage}
                    alt="Original"
                    className="w-full rounded-lg shadow-lg"
                  />
                </div>
                
                <div className="text-center">
                  <h3 className="text-xl font-semibold text-white mb-4">
                    {selectedCelebrity?.name} ({selectedStyle})
                  </h3>
                  <div className="w-full aspect-square bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center text-4xl font-bold text-white shadow-lg">
                    {selectedCelebrity?.name.charAt(0)}
                  </div>
                </div>
                
                <div className="text-center">
                  <h3 className="text-xl font-semibold text-white mb-4">Generated</h3>
                  {generatedImage ? (
                    <img
                      src={generatedImage}
                      alt="Generated"
                      className="w-full rounded-lg shadow-lg"
                    />
                  ) : (
                    <div className="w-full aspect-square bg-gray-300 rounded-lg flex items-center justify-center">
                      <div className="loading-spinner"></div>
                    </div>
                  )}
                </div>
              </div>

              <div className="text-center space-x-4">
                <button
                  onClick={resetApp}
                  className="bg-green-600 hover:bg-green-700 text-white py-3 px-6 rounded-lg font-semibold transition-colors"
                >
                  Try Another Photo
                </button>
                <button
                  onClick={() => setStep(2)}
                  className="bg-blue-600 hover:bg-blue-700 text-white py-3 px-6 rounded-lg font-semibold transition-colors"
                >
                  Choose Different Celebrity
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 text-gray-300">
          <p>Powered by AI • Face Recognition • Image Generation</p>
        </div>
      </div>
    </div>
  );
}

export default App;