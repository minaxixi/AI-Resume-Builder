import axios from 'axios';

// In development, use localhost:5001
// In production, use the environment variable or default to port 8080
const isDevelopment = process.env.NODE_ENV === 'development';
const API_URL = isDevelopment 
  ? (process.env.REACT_APP_API_URL || 'http://localhost:5001')
  : (process.env.REACT_APP_API_URL || window.location.origin);

console.log('API URL:', API_URL);
console.log('Environment:', process.env.NODE_ENV);

export interface TailorResponse {
  original_text: string;
  enhanced_text: string;
}

interface ErrorResponse {
  error: string;
}

export const uploadAndTailorResume = async (
  file: File,
  jobUrl: string
): Promise<TailorResponse> => {
  try {
    console.log('Making request to:', `${API_URL}/tailor-resume`);
    console.log('With job URL:', jobUrl);
    
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_url', jobUrl);

    const response = await axios.post<TailorResponse | ErrorResponse>(`${API_URL}/tailor-resume`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 30000,
      withCredentials: false
    });

    console.log('Response:', response.data);
    const data = response.data;

    if ('error' in data) {
      console.error('Server returned error:', data.error);
      throw new Error(data.error);
    }

    return data as TailorResponse;
  } catch (error) {
    console.error('Full error:', error);
    if (axios.isAxiosError(error)) {
      console.error('Axios error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        config: {
          url: error.config?.url,
          method: error.config?.method,
          headers: error.config?.headers
        }
      });
      if (error.code === 'ECONNABORTED') {
        throw new Error('Request timed out. The server is taking too long to respond. Please try again.');
      }
      throw new Error(error.response?.data?.error || 'Failed to enhance resume. Please try again.');
    }
    throw error;
  }
};
