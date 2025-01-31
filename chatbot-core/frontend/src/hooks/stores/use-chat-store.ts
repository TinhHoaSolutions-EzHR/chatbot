import { create } from 'zustand';

import { IChatMessageResponse, StreamingMessageState } from '@/types/chat';

interface IChatStore {
  userMessage: string;
  isNewChat: boolean;
  chatSession: {
    [id: string]: {
      messages: IChatMessageResponse[];
      streamState: StreamingMessageState;
      streamingMessage: string;
      abortController: AbortController | null;
    };
  };

  initChatSessionIfNotExist(chatSessionId: string): void;
  addMessage(chatSessionId: string, message: IChatMessageResponse): void;
  setStreamState(chatSessionId: string, streamState: StreamingMessageState): void;
  setStreamingMessage(chatSessionId: string, messageChunk: string): void;
  setStreamAbortController(chatSessionId: string, abortController: AbortController | null): void;
  cancelStream(chatSessionId: string): void;

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
      abortController: null,
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
  setStreamAbortController(chatSessionId, abortController) {
    const { chatSession } = get();

    if (!chatSession[chatSessionId]) {
      throw new Error();
    }

    chatSession[chatSessionId].abortController = abortController;

    set({ chatSession });
  },
  cancelStream(chatSessionId) {
    const { chatSession } = get();
    const abortController = chatSession[chatSessionId].abortController;

    if (!chatSession[chatSessionId] || !abortController) {
      throw new Error();
    }

    abortController.abort();
    chatSession[chatSessionId].abortController = null;

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
