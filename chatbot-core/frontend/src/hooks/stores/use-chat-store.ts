import { create } from 'zustand';

interface IChatStore {
  userMessage: string;
  isNewChat: boolean;

  setUserMessage(message: string): void;
  setIsNewChat(isNewChat: boolean): void;

  clearChatStore(): void;
}

const DEFAULT_CHAT_STORE_VALUES = {
  userMessage: '',
  isNewChat: false,
};

export const useChatStore = create<IChatStore>(set => ({
  ...DEFAULT_CHAT_STORE_VALUES,

  setUserMessage(message) {
    set({ userMessage: message });
  },
  setIsNewChat(isNewChat) {
    set({ isNewChat });
  },

  clearChatStore() {
    set({ ...DEFAULT_CHAT_STORE_VALUES });
  },
}));
