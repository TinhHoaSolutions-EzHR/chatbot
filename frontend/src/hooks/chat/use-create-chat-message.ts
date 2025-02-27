import { useMutation, useQueryClient } from '@tanstack/react-query';

import { ReactMutationKey, ReactQueryKey } from '@/constants/react-query-key';
import { createChatMessage } from '@/services/chat/create-chat-message';
import {
  ChatMessageStreamEvent,
  ChatMessageType,
  IChatMessageResponse,
  IChatSession,
  IChatSessionDetail,
  StreamingMessageState,
} from '@/types/chat';
import { checkAbortError } from '@/utils/check-error';
import { decodeChatStreamChunks } from '@/utils/decode-chat-stream-chunk';

import { useChatStore } from '../stores/use-chat-store';

type ChatMessageRequest = Parameters<typeof createChatMessage>[0];

interface IUseCreateChatMessageProps {
  chatSessionId: ChatMessageRequest['chatSessionId'] | undefined | null;
}

export const useCreateChatMessage = ({ chatSessionId }: IUseCreateChatMessageProps) => {
  const setStreamState = useChatStore(state => state.setStreamState);
  const setStreamingMessage = useChatStore(state => state.setStreamingMessage);
  const setStreamAbortController = useChatStore(state => state.setStreamAbortController);
  const initChatSessionIfNotExist = useChatStore(state => state.initChatSessionIfNotExist);

  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: [ReactMutationKey.CREATE_CHAT_MESSAGE, chatSessionId],
    mutationFn: async (props: Omit<ChatMessageRequest, 'abortController'>) => {
      initChatSessionIfNotExist(props.chatSessionId);
      let fullResponse = '';

      try {
        const abortController = new AbortController();
        const stream = await createChatMessage({ ...props, abortController });
        const reader = stream.pipeThrough(new TextDecoderStream()).getReader();
        setStreamAbortController(props.chatSessionId, abortController);

        while (true) {
          const { value, done } = await reader.read();

          if (done) {
            break;
          }

          const chunks = decodeChatStreamChunks(value);

          chunks.forEach(({ event, data }) => {
            switch (event) {
              case ChatMessageStreamEvent.METADATA:
                addChatMessage(data);
                setStreamState(props.chatSessionId, StreamingMessageState.PENDING);
                break;
              case ChatMessageStreamEvent.DELTA:
                if (!fullResponse) {
                  setStreamState(props.chatSessionId, StreamingMessageState.STREAMING);
                }

                fullResponse += data;
                setStreamingMessage(props.chatSessionId, fullResponse);
                break;
              case ChatMessageStreamEvent.TITLE_GENERATION:
                setStreamState(props.chatSessionId, StreamingMessageState.GENERATING_TITLE);
                queryClient.setQueryData([ReactQueryKey.CHAT_SESSIONS], (oldData?: IChatSession[]) => {
                  if (!oldData) {
                    return oldData;
                  }

                  const copiedOldData = [...oldData];

                  const chatSessionIdx = oldData.findIndex(value => value.id === props.chatSessionId);

                  if (chatSessionIdx === -1) {
                    return oldData;
                  }

                  return copiedOldData.map((session, idx) =>
                    idx === chatSessionIdx ? { ...session, description: data } : session,
                  );
                });
                break;
              case ChatMessageStreamEvent.STREAM_COMPLETE:
                const serverChatResponse = {
                  ...data,
                  message: fullResponse,
                };

                addChatMessage(serverChatResponse);
                setStreamState(props.chatSessionId, StreamingMessageState.IDLE);
                break;
            }
          });
        }
      } catch (error) {
        if (checkAbortError(error)) {
          addChatMessage({
            id: window.crypto.randomUUID(),
            message: fullResponse,
            chat_session_id: props.chatSessionId,
            message_type: ChatMessageType.ASSISTANT,
            is_sensitive: false,
            created_at: new Date().toLocaleDateString(),
            updated_at: new Date().toLocaleDateString(),
            deleted_at: null,
          });
        }
        throw error;
      }

      function addChatMessage(chat: IChatMessageResponse) {
        queryClient.setQueryData(
          [ReactQueryKey.CHAT_SESSION, { chatSessionId: props.chatSessionId }],
          (chatSession?: IChatSessionDetail): IChatSessionDetail | undefined => {
            if (!chatSession) {
              return chatSession;
            }

            return {
              ...chatSession,
              chat_messages: [...chatSession.chat_messages, chat],
            };
          },
        );
      }
    },
    onSettled(_, __, variables) {
      setStreamState(variables.chatSessionId, StreamingMessageState.IDLE);
      setStreamAbortController(variables.chatSessionId, null);
    },
  });
};
