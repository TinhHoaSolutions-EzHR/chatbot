export enum ReactQueryKey {
  HEALTH_CHECK = 'health-check',

  CHAT = 'chat',
  CHAT_SESSION = 'chat-session',
  CHAT_SESSIONS = 'chat-sessions',
  CHAT_FOLDERS = 'chat-folders',

  AGENTS = 'agents',
  AGENT = 'agent',
  RECENT_AGENTS = 'recent-agents',

  USER = 'user',
  USER_ACCESS_TOKEN = 'user-access-token',
  USER_SETTINGS = 'user-settings',

  CONNECTORS = 'connectors',
}

export enum ReactMutationKey {
  CREATE_CHAT_FOLDER = 'create-chat-folder',
  EDIT_CHAT_FOLDER = 'edit-chat-folder',
  DELETE_CHAT_FOLDER = 'delete-chat-folder',

  CREATE_CHAT_SESSION = 'create-chat-session',
  EDIT_CHAT_SESSION = 'edit-chat-session',
  DELETE_CHAT_SESSION = 'delete-chat-session',

  CREATE_CHAT_MESSAGE = 'create-chat-message',

  UPLOAD_CONNECTOR_DOCUMENTS = 'upload-connector-documents',
  CREATE_CONNECTOR = 'create-connector',
}
