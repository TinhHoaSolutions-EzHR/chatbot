import { useIsMutating } from '@tanstack/react-query';
import { Check, Pencil, X } from 'lucide-react';
import { FC } from 'react';

import { ReactMutationKey } from '@/constants/react-query-key';
import { cn } from '@/lib/utils';
import { IFolder } from '@/types/chat';

import { DeleteChatFolderButton } from './delete-chat-folder-button';

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
  const isDeletingChatFolder = useIsMutating({
    mutationKey: [ReactMutationKey.DELETE_CHAT_FOLDER],
  });

  return (
    <div
      className={cn(
        'absolute top-0 bottom-0 right-2 gap-2 items-center hidden group-hover/folder:flex',
        !!isDeletingChatFolder && 'pointer-events-none opacity-40',
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
          <DeleteChatFolderButton folder={folder} />
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
