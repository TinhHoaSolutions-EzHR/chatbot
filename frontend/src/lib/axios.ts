import axios, { CreateAxiosDefaults, ResponseType } from 'axios';

import { CHATBOT_CORE_BACKEND_URL, CLIENT_DOMAIN, LOCAL_STORAGE_ACCESS_TOKEN_KEY } from '@/configs/misc';
import { ACCESS_TOKEN_LOCAL_STORAGE_EVENT_DISPATCH, ApiStatusCode } from '@/constants/misc';

const createClient = (responseType: ResponseType, options?: CreateAxiosDefaults<any>) => {
  const client = axios.create({
    baseURL: CHATBOT_CORE_BACKEND_URL,
    headers: {
      'Access-Control-Allow-Origin': CLIENT_DOMAIN,
    },
    responseType,
    withCredentials: true,
    ...options,
  });

  client.interceptors.request.use(config => {
    const accessToken = localStorage.getItem(LOCAL_STORAGE_ACCESS_TOKEN_KEY);

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  });

  client.interceptors.response.use(response => {
    if (response.status === ApiStatusCode.UNAUTHORIZED_404) {
      localStorage.removeItem(LOCAL_STORAGE_ACCESS_TOKEN_KEY);
      window.dispatchEvent(new Event(ACCESS_TOKEN_LOCAL_STORAGE_EVENT_DISPATCH));
    }

    return response;
  });

  return client;
};

const httpClient = createClient('json');
const streamClient = createClient('stream', {
  adapter: 'fetch',
});

export { httpClient, streamClient };
