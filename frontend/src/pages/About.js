import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Cpu, Shield, Zap, Users, Code, Heart } from 'lucide-react';

const About = () => {
  const features = [
    {
      icon: Cpu,
      title: 'Advanced AI Technology',
      description: 'Powered by state-of-the-art face recognition and image processing algorithms.',
    },
    {
      icon: Shield,
      title: 'Privacy First',
      description: 'Your images are processed securely and never stored permanently.',
    },
    {
      icon: Zap,
      title: 'Lightning Fast',
      description: 'Get results in seconds with our optimized processing pipeline.',
    },
    {
      icon: Users,
      title: 'User Friendly',
      description: 'Simple drag-and-drop interface designed for everyone to use.',
    },
  ];

  const technologies = [
    { name: 'React', category: 'Frontend' },
    { name: 'FastAPI', category: 'Backend' },
    { name: 'InsightFace', category: 'AI/ML' },
    { name: 'OpenCV', category: 'Computer Vision' },
    { name: 'Tailwind CSS', category: 'Styling' },
    { name: 'Framer Motion', category: 'Animations' },
  ];

  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center mb-12"
      >
        <h1 className="text-4xl md:text-5xl font-bold mb-6">
          About <span className="gradient-text">AI Image Generator</span>
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          A cutting-edge web application that combines artificial intelligence with creative image processing 
          to transform your photos into stunning artwork and celebrity lookalikes.
        </p>
      </motion.div>

      {/* Mission Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="card mb-12"
      >
        <div className="text-center">
          <Sparkles className="h-12 w-12 text-primary-600 mx-auto mb-4" />
          <h2 className="text-3xl font-bold mb-4">Our Mission</h2>
          <p className="text-lg text-gray-600 leading-relaxed">
            We believe that everyone should have access to powerful AI tools that can unlock their creativity. 
            Our platform makes advanced image processing technology accessible, fun, and easy to use for people 
            of all skill levels.
          </p>
        </div>
      </motion.div>

      {/* Features Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="mb-12"
      >
        <h2 className="text-3xl font-bold text-center mb-8">Why Choose Us</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.6 + index * 0.1 }}
              className="card hover:shadow-xl transition-shadow duration-300"
            >
              <div className="flex items-start space-x-4">
                <div className="bg-primary-100 p-3 rounded-lg">
                  <feature.icon className="h-6 w-6 text-primary-600" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                  <p className="text-gray-600">{feature.description}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Technology Stack */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.6 }}
        className="card mb-12"
      >
        <h2 className="text-3xl font-bold text-center mb-8">Technology Stack</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {technologies.map((tech, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: 0.8 + index * 0.1 }}
              className="bg-gray-50 rounded-lg p-4 text-center hover:bg-gray-100 transition-colors duration-200"
            >
              <div className="font-semibold text-gray-900">{tech.name}</div>
              <div className="text-sm text-gray-500">{tech.category}</div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* How It Works */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.8 }}
        className="card mb-12"
      >
        <h2 className="text-3xl font-bold text-center mb-8">How It Works</h2>
        <div className="space-y-8">
          <div className="flex items-start space-x-4">
            <div className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
              1
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-2">Upload Your Photo</h3>
              <p className="text-gray-600">
                Simply drag and drop or click to upload a clear photo with a visible face. 
                Our system automatically detects and validates the image quality.
              </p>
            </div>
          </div>
          
          <div className="flex items-start space-x-4">
            <div className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
              2
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-2">Choose Your Style</h3>
              <p className="text-gray-600">
                Select between finding a celebrity lookalike or transforming your photo into 
                various cartoon styles including anime, comic book, and sketch effects.
              </p>
            </div>
          </div>
          
          <div className="flex items-start space-x-4">
            <div className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
              3
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-2">AI Processing</h3>
              <p className="text-gray-600">
                Our advanced AI algorithms analyze facial features, apply artistic transformations, 
                and generate high-quality results in just seconds.
              </p>
            </div>
          </div>
          
          <div className="flex items-start space-x-4">
            <div className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
              4
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-2">Download & Share</h3>
              <p className="text-gray-600">
                Download your AI-generated image in high quality and share it with friends 
                and family. All results are ready for immediate use.
              </p>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Privacy & Security */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 1.0 }}
        className="card mb-12 bg-blue-50 border-blue-200"
      >
        <div className="text-center">
          <Shield className="h-12 w-12 text-blue-600 mx-auto mb-4" />
          <h2 className="text-3xl font-bold mb-4 text-blue-900">Privacy & Security</h2>
          <p className="text-lg text-blue-800 leading-relaxed">
            Your privacy is our top priority. We process images securely and do not store them permanently. 
            All uploaded images are automatically deleted after processing, and we never share your data 
            with third parties.
          </p>
        </div>
      </motion.div>

      {/* Call to Action */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 1.2 }}
        className="text-center"
      >
        <div className="bg-gradient-to-r from-primary-600 to-secondary-600 rounded-xl p-8 text-white">
          <Heart className="h-12 w-12 mx-auto mb-4" />
          <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
          <p className="text-xl mb-6 opacity-90">
            Join thousands of users who are already creating amazing AI-generated images!
          </p>
          <a
            href="/"
            className="inline-block bg-white text-primary-600 font-semibold px-8 py-3 rounded-lg hover:bg-gray-100 transition-colors duration-200"
          >
            Start Creating Now
          </a>
        </div>
      </motion.div>
    </div>
  );
};

export default About;