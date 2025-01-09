import { create } from 'zustand';

export enum DialogType {
  NONE = 'none',
  CREATE_CHAT_FOLDER = 'create-chat-folder',
}

interface IDialogStore {
  dialogType: DialogType;
  openDialog(dialogType: DialogType): void;
  closeDialog(): void;
}

export const useDialogStore = create<IDialogStore>(set => ({
  dialogType: DialogType.NONE,
  openDialog(dialogType) {
    set({ dialogType });
  },
  closeDialog() {
    set({ dialogType: DialogType.NONE });
  },
}));
