import { create } from 'zustand';

import { IChatMessageResponse, StreamingMessageState } from '@/types/chat';

interface IChatStore {
  userMessage: string;
  isNewChat: boolean;
  chatSession: {
    [id: string]:
      | {
          messages: IChatMessageResponse[];
          streamState: StreamingMessageState;
          streamingMessage: string;
        }
      | undefined;
  };

  initChatSessionIfNotExist(chatSessionId: string): void;
  addMessage(chatSessionId: string, message: IChatMessageResponse): void;
  setStreamState(chatSessionId: string, streamState: StreamingMessageState): void;
  setStreamingMessage(chatSessionId: string, messageChunk: string): void;

  setUserMessage(message: string): void;
  setIsNewChat(isNewChat: boolean): void;

  clearUserNewChat(): void;
}

const DEFAULT_USER_CHAT_VALUES = {
  userMessage: '',
  isNewChat: false,
};

export const useChatStore = create<IChatStore>((set, get) => ({
  ...DEFAULT_USER_CHAT_VALUES,
  chatSession: {},

  initChatSessionIfNotExist(chatSessionId) {
    const { chatSession } = get();

    if (chatSession[chatSessionId]) {
      return;
    }

    chatSession[chatSessionId] = {
      messages: [],
      streamState: StreamingMessageState.IDLE,
      streamingMessage: '',
    };

    set({ chatSession });
  },
  addMessage(chatSessionId, message) {
    const { chatSession } = get();

    if (!chatSession[chatSessionId]) {
      throw new Error();
    }

    const messages = chatSession[chatSessionId].messages;

    chatSession[chatSessionId].messages = [...messages, message];

    set({ chatSession });
  },
  setStreamState(chatSessionId, streamState) {
    const { chatSession } = get();

    if (!chatSession[chatSessionId]) {
      throw new Error();
    }

    chatSession[chatSessionId].streamState = streamState;

    set({ chatSession });
  },
  setStreamingMessage(chatSessionId, messageChunk) {
    const { chatSession } = get();

    if (!chatSession[chatSessionId]) {
      throw new Error();
    }

    chatSession[chatSessionId].streamingMessage = messageChunk;

    set({ chatSession });
  },

  setUserMessage(message) {
    set({ userMessage: message });
  },
  setIsNewChat(isNewChat) {
    set({ isNewChat });
  },

  clearUserNewChat() {
    set({ ...DEFAULT_USER_CHAT_VALUES });
  },
}));
