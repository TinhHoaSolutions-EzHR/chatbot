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
  folder_id?: string | null;
  shared_status: ChatSessionSharedStatus;
  created_at: string;
  updated_at: string;
  deleted_at?: string;
}

export interface IChatSessionRequest {
  agent_id: string;
  folder_id: string | null;
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

export interface IChatMessageResponse {
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

export enum ChatMessageStreamEvent {
  METADATA = 'metadata',
  DELTA = 'delta',
  STREAM_COMPLETE = 'stream_complete',
  ERROR = 'error',
}

export type ChatStreamChunk =
  | {
      event: ChatMessageStreamEvent.METADATA;
      data: IChatMessageResponse;
    }
  | {
      event: ChatMessageStreamEvent.DELTA;
      data: string;
    }
  | {
      event: ChatMessageStreamEvent.STREAM_COMPLETE;
      data: Omit<IChatMessageResponse, 'message'>;
    }
  | {
      event: ChatMessageStreamEvent.ERROR;
      data: string;
    };

export interface IFolder {
  id: string;
  user_id: string;
  name?: string;
  display_priority?: number;
}
