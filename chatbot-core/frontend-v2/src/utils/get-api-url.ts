import { API_VERSION, CHATBOT_CORE_BACKEND_URL } from '@/configs/misc';

export enum ApiEndpointPrefix {
  USER = '/users/me',
}

export const AUTH_PREFIX = '/auth';

export const getApiUrl = (prefix: ApiEndpointPrefix, endpoint?: string) => {
  return `${CHATBOT_CORE_BACKEND_URL}/api/${API_VERSION}/${prefix}${endpoint ?? ''}`;
};

export const getAuthUrl = (endpoint: string) => {
  return `${CHATBOT_CORE_BACKEND_URL}/${AUTH_PREFIX}${endpoint}`;
};

export const getHealthCheckUrl = () => {
  return `${CHATBOT_CORE_BACKEND_URL}/health`;
};
