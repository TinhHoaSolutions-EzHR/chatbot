import { QueryClient, useMutation, useQueryClient } from '@tanstack/react-query';

import { ReactMutationKey, ReactQueryKey } from '@/constants/react-query-key';
import { editChatSession } from '@/services/chat/edit-chat-session';
import { IChatSession } from '@/types/chat';

type TEditChatSessionProps = Parameters<typeof editChatSession>[0];

const modifyCachedData = (queryClient: QueryClient, modifiedData: TEditChatSessionProps) => {
  let isModified = true;

  queryClient.setQueryData([ReactQueryKey.CHAT_SESSIONS], (oldData?: IChatSession[]) => {
    if (!oldData) {
      return oldData;
    }

    const copyOldData = [...oldData];

    const patchedFolderIndex = copyOldData.findIndex(value => value.id === modifiedData.chatSessionId);

    // Found the folder with new name in the tanstack cached data, should assign a new one,
    // if cannot find (due to several reasons, but this should not happened), refetch the query
    if (~patchedFolderIndex) {
      const previousValue = copyOldData[patchedFolderIndex];
      copyOldData[patchedFolderIndex] = { ...previousValue, ...modifiedData.data };
    } else {
      isModified = false;
    }

    return copyOldData;
  });

  return isModified;
};

export const useEditChatSession = (shouldUpdateCacheBeforeFetch?: boolean) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: [ReactMutationKey.EDIT_CHAT_SESSION],
    mutationFn: (props: TEditChatSessionProps) => {
      if (shouldUpdateCacheBeforeFetch) {
        modifyCachedData(queryClient, props);
      }

      return editChatSession(props);
    },
    onSuccess(data, { chatSessionId }) {
      const isModified = modifyCachedData(queryClient, {
        chatSessionId,
        data,
      });

      if (!isModified) {
        queryClient.invalidateQueries({
          queryKey: [ReactQueryKey.CHAT_SESSIONS],
          type: 'active',
        });
      }
    },
    onError() {
      if (shouldUpdateCacheBeforeFetch) {
        queryClient.invalidateQueries({
          queryKey: [ReactQueryKey.CHAT_SESSIONS],
          type: 'active',
        });
      }
    },
  });
};
