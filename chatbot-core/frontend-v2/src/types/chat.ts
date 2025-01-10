export enum ChatSessionSharedStatus {
  PUBLIC = 'public',
  PRIVATE = 'private',
}

export enum ChatMessageType {
  SYSTEM = 'system',
  USER = 'user',
  ASSISTANT = 'assistant',
}

export interface IChatSession {
  id: string;
  description?: string;
  user_id: string;
  agent_id?: string;
  folder_id?: string;
  shared_status: ChatSessionSharedStatus;
  created_at: string;
  updated_at: string;
  deleted_at?: string;
}

export interface IChatSessionRequest {
  agent_id: string;
  folder_id: string;
  description: string;
  shared_status: ChatSessionSharedStatus;
}

export enum ChatMessageRequestType {
  NEW = 'new',
  REGENERATE = 'regenerate',
  EDIT = 'edit',
}

export interface IChatMessageRequest {
  id: string;
  message: string;
  is_sensitive: boolean;
  parent_message_id: string;
  chat_message_request_type: ChatMessageRequestType;
}

interface IChatMessageResponse {
  id: string;
  chat_session_id: string;
  message: string;
  message_type: ChatMessageType;
  parent_message_id?: string;
  child_message_id?: string;
  is_sensitive: boolean;
  created_at: string;
  updated_at: string;
}

export interface IChatSessionDetail extends IChatSession {
  messages?: IChatMessageResponse[];
}

export interface IFolder {
  id: string;
  user_id: string;
  name?: string;
  display_priority?: number;
}
