export enum SupportedKeys {
  ENTER = 'Enter',
  ESCAPE = 'Escape',
}

export enum ApiStatusCode {
  UNAUTHORIZED_404 = 404,
}

export enum QueryParams {
  OAUTH_CODE = 'code',
  CHAT_SESSION_ID = 's',
}

export const ACCESS_TOKEN_LOCAL_STORAGE_EVENT_DISPATCH = 'access-token-local-storage';

export enum Route {
  HOME_PAGE = '/',
  CHAT = '/chat',
  MANAGE_ASSISTANTS = '/manage-assistants',

  ADMIN = '/admin',
  EXISTING_CONNECTORS = '/admin/existing-connectors',
  ADD_CONNECTOR = '/admin/add-connector',

  NOT_SUPPORTED = '/not-supported',
  SUPPORTS = '/supports',
}
