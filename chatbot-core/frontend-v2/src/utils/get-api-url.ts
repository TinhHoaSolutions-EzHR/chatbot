import { API_VERSION } from '@/configs/misc';

export enum ApiEndpointPrefix {
  USER = '/users/me',
  CHAT = '/chat',
  FOLDER = '/folders',
  AGENTS = '/agents',
}

export enum AuthEndpoint {
  GOOGLE_OAUTH = '/auth/oauth/google',
}

export const getApiUrl = (prefix: ApiEndpointPrefix, endpoint?: string) => {
  return `/api/${API_VERSION}${prefix}${endpoint ?? ''}`;
};
