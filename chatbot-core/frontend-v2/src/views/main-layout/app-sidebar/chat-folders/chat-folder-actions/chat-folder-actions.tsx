import { FC, useEffect, useState } from 'react';
import { toast } from 'sonner';

import { SidebarMenuButton } from '@/components/ui/sidebar';
import { useEditChatFolder } from '@/hooks/chat/use-edit-chat-folder';
import { IFolder } from '@/types/chat';

import { FolderActionsButtons } from './folder-actions-buttons';
import { FolderNameInput } from './folder-name-input';

interface IChatFolderActionsProps {
  isFolderOpen: boolean;
  folder: IFolder;
}

export const ChatFolderActions: FC<IChatFolderActionsProps> = ({ folder, isFolderOpen }) => {
  const [isEditingFolder, setIsEditingFolder] = useState<boolean>(false);

  const [folderName, setFolderName] = useState('');

  const { mutate, isPending } = useEditChatFolder(folder.id);

  useEffect(() => {
    if (isEditingFolder && folder.name) {
      setFolderName(folder.name);
    }
  }, [isEditingFolder]);

  const onEditChatFolder = () => {
    if (!folderName.length) {
      toast.error('Folder name must not be left blanked');
    }

    mutate(
      { folderId: folder.id, folderName },
      {
        onSuccess() {
          toast.success('Edit folder name successfully!');
          setIsEditingFolder(false);
        },
        onError() {
          toast.error('Edit folder name failed', {
            description: "There's something wrong with your request. Please try again later!",
          });
        },
      },
    );
  };

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
