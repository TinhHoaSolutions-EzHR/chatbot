import { useMutation, useQueryClient } from '@tanstack/react-query';

import { ReactMutationKey, ReactQueryKey } from '@/constants/react-query-key';
import { editChatSession } from '@/services/chat/edit-chat-session';
import { IChatSession, IChatSessionRequest } from '@/types/chat';

export const useEditChatSession = (chatSessionId: string, data: Partial<IChatSessionRequest>) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: [ReactMutationKey.EDIT_CHAT_SESSION],
    mutationFn: () => editChatSession(chatSessionId, data),
    onSuccess(data) {
      queryClient.setQueryData([ReactQueryKey.CHAT_SESSIONS], (oldData?: IChatSession[]) => {
        if (!oldData) {
          return oldData;
        }

        const copyOldData = [...oldData];

        const patchedFolderIndex = copyOldData.findIndex(value => value.id === chatSessionId);

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
