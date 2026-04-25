import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000/api';

export const analyzeContent = async (type, content) => {
  const response = await axios.post(`${API_BASE}/analyze/`, {
    type,
    content
  });
  return response.data;
};