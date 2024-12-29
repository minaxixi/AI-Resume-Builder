import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';  

interface TailorResponse {
  original_resume: string;
  tailored_resume: string;
}

interface ErrorResponse {
  error: string;
  details?: string;
}

export const tailorResume = async (resume: File, jobDescription: string): Promise<TailorResponse> => {
  const formData = new FormData();
  formData.append('resume', resume);
  formData.append('job_description', jobDescription);

  console.log('Sending request to:', `${API_URL}/tailor-resume`);
  console.log('File being sent:', resume);
  console.log('Job description:', jobDescription);

  try {
    const response = await axios.post<TailorResponse | ErrorResponse>(`${API_URL}/tailor-resume`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 30000,
      validateStatus: (status) => status < 500,
    });

    console.log('Response received:', response.data);
    
    if (response.status !== 200) {
      const errorData = response.data as ErrorResponse;
      throw new Error(errorData.error || 'Failed to process resume');
    }
    
    return response.data as TailorResponse;
  } catch (error: any) {
    console.error('API Error:', error);
    if (axios.isAxiosError(error)) {
      const errorMessage = error.response?.data?.error || error.message;
      throw new Error(errorMessage);
    } else if (error.code === 'ECONNABORTED') {
      throw new Error('Request timed out. Please try again.');
    } else if (!navigator.onLine) {
      throw new Error('No internet connection. Please check your network.');
    } else {
      throw new Error('Network error. Please check if the backend server is running.');
    }
  }
};
