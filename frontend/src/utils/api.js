import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000/api';

export const analyzeContent = async (type, content) => {
  const response = await axios.post(`${API_BASE}/analyze/`, {
    type,
    content
  });
  return response.data;
};
export const cleanWhatsAppText = (text) => {
  // Remove emojis
  text = text.replace(/[\u{1F600}-\u{1F64F}]/gu, '')
  text = text.replace(/[\u{1F300}-\u{1F5FF}]/gu, '')
  text = text.replace(/[\u{1F680}-\u{1F6FF}]/gu, '')
  text = text.replace(/[\u{2600}-\u{26FF}]/gu, '')
  text = text.replace(/[\u{2700}-\u{27BF}]/gu, '')

  // Remove forwarded message header
  text = text.replace(/Forwarded message/gi, '')
  text = text.replace(/Forwarded many times/gi, '')
  text = text.replace(/\[.*?\]/g, '')  // Remove [brackets]

  // Clean extra whitespace
  text = text.replace(/\n{3,}/g, '\n\n')
  text = text.trim()

  return text
}

export const detectLanguage = (text) => {
  // Gujarati unicode range: \u0A80-\u0AFF
  const gujaratiChars = text.match(/[\u0A80-\u0AFF]/g)
  if (gujaratiChars && gujaratiChars.length > 10) {
    return 'gujarati'
  }
  return 'english'
}