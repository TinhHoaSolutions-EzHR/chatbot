import { Check, Pencil, Trash2, X } from 'lucide-react';
import { FC } from 'react';

import { DialogType, useDialogStore } from '@/hooks/stores/use-dialog-store';
import { cn } from '@/lib/utils';
import { IFolder } from '@/types/chat';

interface IFolderActionsButtonsProps {
  folder: IFolder;
  isEditingFolder: boolean;
  setIsEditingFolder(isEditingFolder: boolean): void;
  onEditChatFolder(): void;
  isPending: boolean;
}

export const FolderActionsButtons: FC<IFolderActionsButtonsProps> = ({
  folder,
  isEditingFolder,
  setIsEditingFolder,
  onEditChatFolder,
  isPending,
}) => {
  const { openDialog } = useDialogStore();
  return (
    <div
      className={cn(
        'absolute top-0 bottom-0 right-2 gap-2 items-center hidden group-hover/folder:flex',
        isEditingFolder && 'flex',
      )}
    >
      {!isEditingFolder ? (
        <>
          <Pencil
            size={14}
            className="text-muted-foreground hover:text-zinc-800"
            onClick={() => setIsEditingFolder(true)}
          />
          <Trash2
            size={14}
            className="text-muted-foreground hover:text-zinc-800"
            onClick={() => openDialog(DialogType.DELETE_CHAT_FOLDER, { folder })}
          />
        </>
      ) : (
        <>
          <Check size={14} className="text-muted-foreground hover:text-zinc-800" onClick={onEditChatFolder} />
          <X
            size={14}
            className="text-muted-foreground hover:text-zinc-800"
            onClick={() => !isPending && setIsEditingFolder(false)}
          />
        </>
      )}
    </div>
  );
};
