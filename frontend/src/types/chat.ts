import { ITimestampResponse } from './common';

export enum ChatSessionSharedStatus {
  PUBLIC = 'public',
  PRIVATE = 'private',
}

export enum ChatMessageType {
  SYSTEM = 'system',
  USER = 'user',
  ASSISTANT = 'assistant',
}

export interface IChatSession extends ITimestampResponse {
  id: string;
  description?: string;
  user_id: string;
  agent_id?: string;
  folder_id?: string | null;
  shared_status: ChatSessionSharedStatus;
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

export interface IChatMessageResponse extends ITimestampResponse {
  id: string;
  chat_session_id: string;
  message: string;
  message_type: ChatMessageType;
  parent_message_id?: string;
  child_message_id?: string;
  is_sensitive: boolean;
}

export interface IChatSessionDetail extends IChatSession {
  chat_messages: IChatMessageResponse[];
}

/*
 * The event received from server through SSE after user create chat message.
 * These events can be:
 * - metadata: the user's request message.
 * - delta: the server's encoding chat response.
 * - title_generation: the chat title after complete
 * - stream_complete: the signal indicating the SSE close, and return the chat response object but exclude the message field.
 * - error: error occurred on the server side.
 */
export enum ChatMessageStreamEvent {
  METADATA = 'metadata',
  DELTA = 'delta',
  TITLE_GENERATION = 'title_generation',
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
      event: ChatMessageStreamEvent.TITLE_GENERATION;
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

export enum StreamingMessageState {
  IDLE = 'idle',
  PENDING = 'pending',
  STREAMING = 'streaming',
  GENERATING_TITLE = 'generating-title',
}

export interface IFolder {
  id: string;
  user_id: string;
  name?: string;
  display_priority?: number;
}
