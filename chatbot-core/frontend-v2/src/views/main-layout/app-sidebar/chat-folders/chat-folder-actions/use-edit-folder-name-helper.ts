import { useEffect, useState } from 'react';
import { toast } from 'sonner';

import { useEditChatFolder } from '@/hooks/chat/use-edit-chat-folder';
import { IFolder } from '@/types/chat';

export const useEditFolderNameHelper = (folder: IFolder) => {
  const [isEditingFolder, setIsEditingFolder] = useState<boolean>(false);

  const [folderName, setFolderName] = useState<string>('');

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

  return {
    folderName,
    setFolderName,
    isEditingFolder,
    setIsEditingFolder,
    onEditChatFolder,
    isPending,
  };
};
