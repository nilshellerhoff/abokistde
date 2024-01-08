import axios from 'axios';
import { getBaseApiUrl } from 'src/util/host';

const getAuthorizationHeaders = () => {
  const cookies = document.cookie.split(';');
  const headers: Record<string, string> = {};
  cookies.forEach((cookie) => {
    const [key, value] = cookie.split('=');
    if (key.trim() == 'csrftoken') {
      headers['X-CSRFToken'] = value.trim();
    }
  });
  return headers;
};

export const apiClient = axios.create({
  // baseURL: process.env.API_BASE_URL,
  // baseURL: 'http://localhost:8000/api', // TODO
  baseURL: getBaseApiUrl(),
  headers: getAuthorizationHeaders(),
  withCredentials: true,
});
