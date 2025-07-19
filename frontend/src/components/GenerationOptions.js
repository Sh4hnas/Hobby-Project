import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { User, Palette, Sparkles, ChevronDown } from 'lucide-react';

const GenerationOptions = ({ onGenerate, isProcessing }) => {
  const [selectedStyle, setSelectedStyle] = useState('cartoon');
  const [showStyleOptions, setShowStyleOptions] = useState(false);

  const cartoonStyles = [
    { id: 'cartoon', name: 'Classic Cartoon', description: 'Traditional cartoon style with bold outlines' },
    { id: 'anime', name: 'Anime Style', description: 'Japanese animation style with smooth shading' },
    { id: 'comic', name: 'Comic Book', description: 'Comic book style with dramatic effects' },
    { id: 'sketch', name: 'Pencil Sketch', description: 'Artistic pencil sketch effect' },
  ];

  const handleGenerate = (type) => {
    if (type === 'cartoon') {
      onGenerate('cartoon', { style: selectedStyle });
    } else {
      onGenerate('famous-person');
    }
  };

  return (
    <div className="space-y-6">
      {/* Famous Person Generation */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold flex items-center space-x-2">
          <User className="h-5 w-5 text-primary-600" />
          <span>Famous Person Match</span>
        </h3>
        <p className="text-gray-600 text-sm">
          Find a celebrity who looks similar to you using AI face recognition.
        </p>
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => handleGenerate('famous-person')}
          disabled={isProcessing}
          className="w-full btn-primary flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Sparkles className="h-4 w-4" />
          <span>Find My Celebrity Lookalike</span>
        </motion.button>
      </div>

      {/* Divider */}
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-gray-300" />
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="px-2 bg-white text-gray-500">or</span>
        </div>
      </div>

      {/* Cartoon Generation */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold flex items-center space-x-2">
          <Palette className="h-5 w-5 text-primary-600" />
          <span>Cartoon Style</span>
        </h3>
        <p className="text-gray-600 text-sm">
          Transform your photo into a cartoon character with various artistic styles.
        </p>

        {/* Style Selector */}
        <div className="relative">
          <button
            onClick={() => setShowStyleOptions(!showStyleOptions)}
            className="w-full flex items-center justify-between p-3 border border-gray-300 rounded-lg bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <span className="text-left">
              <span className="block font-medium">
                {cartoonStyles.find(s => s.id === selectedStyle)?.name}
              </span>
              <span className="text-sm text-gray-500">
                {cartoonStyles.find(s => s.id === selectedStyle)?.description}
              </span>
            </span>
            <ChevronDown 
              className={`h-5 w-5 text-gray-400 transition-transform ${
                showStyleOptions ? 'rotate-180' : ''
              }`} 
            />
          </button>

          {/* Style Options Dropdown */}
          {showStyleOptions && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg"
            >
              {cartoonStyles.map((style) => (
                <button
                  key={style.id}
                  onClick={() => {
                    setSelectedStyle(style.id);
                    setShowStyleOptions(false);
                  }}
                  className={`w-full text-left p-3 hover:bg-gray-50 first:rounded-t-lg last:rounded-b-lg ${
                    selectedStyle === style.id ? 'bg-primary-50 text-primary-700' : ''
                  }`}
                >
                  <div className="font-medium">{style.name}</div>
                  <div className="text-sm text-gray-500">{style.description}</div>
                </button>
              ))}
            </motion.div>
          )}
        </div>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => handleGenerate('cartoon')}
          disabled={isProcessing}
          className="w-full btn-primary flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Sparkles className="h-4 w-4" />
          <span>Generate Cartoon</span>
        </motion.button>
      </div>

      {/* Processing Note */}
      {isProcessing && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center text-sm text-gray-500"
        >
          <p>Processing may take 10-30 seconds depending on image complexity...</p>
        </motion.div>
      )}
    </div>
  );
};

export default GenerationOptions;