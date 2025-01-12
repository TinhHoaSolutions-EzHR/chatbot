import { FC } from 'react';

import { SidebarMenuButton } from '@/components/ui/sidebar';
import { IFolder } from '@/types/chat';

import { FolderActionsButtons } from './folder-actions-buttons';
import { FolderNameInput } from './folder-name-input';
import { useEditFolderNameHelper } from './use-edit-folder-name-helper';

interface IChatFolderActionsProps {
  isFolderOpen: boolean;
  folder: IFolder;
}

export const ChatFolderActions: FC<IChatFolderActionsProps> = ({ folder, isFolderOpen }) => {
  const { folderName, setFolderName, isEditingFolder, onEditChatFolder, isPending, setIsEditingFolder } =
    useEditFolderNameHelper(folder);

  return (
    <SidebarMenuButton className="relative group/folder">
      <FolderNameInput
        isFolderOpen={isFolderOpen}
        folder={folder}
        isEditingFolder={isEditingFolder}
        onEditChatFolder={onEditChatFolder}
        isPending={isPending}
        folderName={folderName}
        setFolderName={setFolderName}
      />
      <FolderActionsButtons
        folder={folder}
        isEditingFolder={isEditingFolder}
        setIsEditingFolder={setIsEditingFolder}
        onEditChatFolder={onEditChatFolder}
        isPending={isPending}
      />
    </SidebarMenuButton>
  );
};
