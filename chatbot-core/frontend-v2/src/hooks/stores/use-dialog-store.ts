import { create } from 'zustand';

import { IChatSession, IFolder } from '@/types/chat';

export enum DialogType {
  NONE = 'none',

  CREATE_CHAT_FOLDER = 'create-chat-folder',
  DELETE_CHAT_FOLDER = 'delete-chat-folder',

  MOVE_CHAT_SESSION = 'move-chat-session',
  DELETE_CHAT_SESSION = 'delete-chat-session',
}

const CLEAR_STORE_DATA_TIMEOUT = 500;

interface IDialogStoreData {
  chatSession: IChatSession;
  folder: IFolder;
}

interface IDialogStore {
  dialogType: DialogType;
  data: Partial<IDialogStoreData>;
  openDialog(dialogType: DialogType, data?: Partial<IDialogStoreData>): void;
  closeDialog(): void;
}

export const useDialogStore = create<IDialogStore>(set => ({
  dialogType: DialogType.NONE,
  data: {},
  openDialog(dialogType, data) {
    set({ dialogType, data });
  },
  closeDialog() {
    set({ dialogType: DialogType.NONE });
    setTimeout(() => {
      set({ data: {} });
    }, CLEAR_STORE_DATA_TIMEOUT);
  },
}));
