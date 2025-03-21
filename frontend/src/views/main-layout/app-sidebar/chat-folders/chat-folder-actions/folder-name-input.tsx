import { FolderClosed, FolderOpen } from 'lucide-react';
import { FC } from 'react';

import { SupportedKeys } from '@/constants/misc';
import { cn } from '@/lib/utils';
import { IFolder } from '@/types/chat';

interface IFolderNameInputProps {
  isFolderOpen: boolean;
  isEditingFolder: boolean;
  setIsEditingFolder(isEditing: boolean): void;
  folder: IFolder;
  folderName: string;
  setFolderName(folderName: string): void;
  onEditChatFolder(): void;
  isPending: boolean;
}

export const FolderNameInput: FC<IFolderNameInputProps> = ({
  isFolderOpen,
  isEditingFolder,
  setIsEditingFolder,
  folder,
  folderName,
  setFolderName,
  onEditChatFolder,
  isPending,
}) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === SupportedKeys.ESCAPE) {
      setIsEditingFolder(false);
      return;
    }

    if (e.key === SupportedKeys.ENTER) {
      onEditChatFolder();
    }
  };

  return (
    <>
      {isFolderOpen ? <FolderOpen /> : <FolderClosed />}
      {isEditingFolder ? (
        <input
          className={cn(
            'w-32 border border-solid border-zinc-200 rounded p-[2px] cursor-text',
            !!isPending && 'pointer-events-none',
          )}
          value={folderName}
          onChange={e => setFolderName(e.target.value)}
          onKeyDown={handleKeyDown}
          autoFocus
        />
      ) : (
        folder.name
      )}
    </>
  );
};
