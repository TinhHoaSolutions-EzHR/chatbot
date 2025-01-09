import axios from 'axios';

import { CHATBOT_CORE_BACKEND_URL, LOCAL_STORAGE_ACCESS_TOKEN_KEY } from '@/configs/misc';
import { ACCESS_TOKEN_LOCAL_STORAGE_EVENT_DISPATCH, ApiStatusCode } from '@/constants/misc';

const httpClient = axios.create({
  baseURL: CHATBOT_CORE_BACKEND_URL,
  headers: {
    'Access-Control-Allow-Origin': 'http://localhost:3000',
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

httpClient.interceptors.request.use(config => {
  const accessToken = localStorage.getItem(LOCAL_STORAGE_ACCESS_TOKEN_KEY);

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  return config;
});

httpClient.interceptors.response.use(response => {
  if (response.status === ApiStatusCode.UNAUTHORIZED_404) {
    localStorage.removeItem(LOCAL_STORAGE_ACCESS_TOKEN_KEY);
    window.dispatchEvent(new Event(ACCESS_TOKEN_LOCAL_STORAGE_EVENT_DISPATCH));
  }

  return response;
});

export default httpClient;
