import { create } from 'zustand';

interface IChatStore {
  message: string;
  isNewMessage: boolean;
  chatSessionId: string;

  setMessage(message: string): void;
  setIsNewMessage(isNewMessage: boolean): void;
  setChatSessionId(chatSessionId: string): void;

  clearChatStore(): void;
}

const DEFAULT_CHAT_STORE_VALUES = {
  message: '',
  isNewMessage: false,
  chatSessionId: '',
};

export const useChatStore = create<IChatStore>(set => ({
  ...DEFAULT_CHAT_STORE_VALUES,

  setMessage(message) {
    set({ message });
  },
  setIsNewMessage(isNewMessage) {
    set({ isNewMessage });
  },
  setChatSessionId(chatSessionId) {
    set({ chatSessionId });
  },

  clearChatStore() {
    set({ ...DEFAULT_CHAT_STORE_VALUES });
  },
}));
