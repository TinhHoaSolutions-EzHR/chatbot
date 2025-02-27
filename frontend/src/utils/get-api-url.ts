import { API_VERSION } from '@/configs/misc';

export enum ApiEndpointPrefix {
  USER = '/users/me',
  CHAT = '/chat',
  FOLDER = '/folders',
  AGENTS = '/agents',
  CONNECTORS = '/connectors',
  DOCUMENTS = '/documents',
  BACKGROUND_TASKS = '/background/tasks',
}

export enum AuthEndpoint {
  GOOGLE_OAUTH = '/auth/oauth/google',
}

export const getApiUrl = (prefix: ApiEndpointPrefix, endpoint?: string) => {
  return `/api/${API_VERSION}${prefix}${endpoint ?? ''}`;
};
