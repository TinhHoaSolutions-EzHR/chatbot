export enum ReactQueryKey {
  HEALTH_CHECK = 'health-check',

  CHAT = 'chat',
  CHAT_SESSIONS = 'chat-sessions',
  CHAT_FOLDERS = 'chat-folders',

  AGENTS = 'agents',
  AGENT = 'agent',
  RECENT_AGENTS = 'recent-agents',

  USER = 'user',
  USER_ACCESS_TOKEN = 'user-access-token',
}

export enum ReactMutationKey {
  CREATE_CHAT_FOLDER = 'create-chat-folder',
  EDIT_CHAT_FOLDER = 'edit-chat-folder',
  DELETE_CHAT_FOLDER = 'delete-chat-folder',
}
