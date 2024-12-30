import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';  

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
        status: error.response?.status
      });
      if (error.code === 'ECONNABORTED') {
        throw new Error('Request timed out. The server is taking too long to respond. Please try again.');
      }
      throw new Error(error.response?.data?.error || 'Failed to enhance resume. Please try again.');
    }
    throw error;
  }
};
