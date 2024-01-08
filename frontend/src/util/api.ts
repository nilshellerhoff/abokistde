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
  baseURL: getBaseApiUrl(),
  headers: getAuthorizationHeaders(),
  withCredentials: true,
});
