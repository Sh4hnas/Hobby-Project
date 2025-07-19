import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 60000, // 60 seconds timeout for image processing
});

// Request interceptor to add loading states
api.interceptors.request.use(
  (config) => {
    // You could add loading indicators here
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle different types of errors
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.detail || error.response.data?.message || 'Server error occurred';
      throw new Error(message);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('No response from server. Please check your connection.');
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred.');
    }
  }
);

// API functions
export const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/upload-image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const generateFamousPerson = async (filename) => {
  const formData = new FormData();
  formData.append('filename', filename);

  const response = await api.post('/generate-famous-person', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });

  return response.data;
};

export const generateCartoon = async (filename, style = 'cartoon') => {
  const formData = new FormData();
  formData.append('filename', filename);
  formData.append('style', style);

  const response = await api.post('/generate-cartoon', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });

  return response.data;
};

export const downloadImage = async (filename) => {
  const response = await api.get(`/download/${filename}`, {
    responseType: 'blob',
  });

  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;