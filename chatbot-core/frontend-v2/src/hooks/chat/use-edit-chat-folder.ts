import { useMutation, useQueryClient } from '@tanstack/react-query';
import cloneDeep from 'lodash/cloneDeep';

import { ReactMutationKey, ReactQueryKey } from '@/constants/react-query-key';
import { editChatFolder } from '@/services/chat/edit-chat-folder';
import { IFolder } from '@/types/chat';

export const useEditChatFolder = (folderId: string, folderName: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => editChatFolder(folderId, folderName),
    mutationKey: [ReactMutationKey.EDIT_CHAT_FOLDER],
    onSuccess(data) {
      queryClient.setQueryData([ReactQueryKey.CHAT_FOLDERS], (oldData?: IFolder[]) => {
        if (!oldData) {
          return oldData;
        }

        const copyOldData = cloneDeep(oldData);

        const patchedFolderIndex = copyOldData.findIndex(value => value.id === folderId);

        // Found the folder with new name in the tanstack cached data, should assign a new one,
        // if cannot find (due to several reasons, but this should not happened), refetch the query
        if (~patchedFolderIndex) {
          copyOldData[patchedFolderIndex] = data;
        } else {
          queryClient.invalidateQueries({
            queryKey: [ReactQueryKey.CHAT_FOLDERS],
          });
        }

        return copyOldData;
      });
    },
  });
};
