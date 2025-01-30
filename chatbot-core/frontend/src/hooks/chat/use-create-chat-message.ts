import { useMutation } from '@tanstack/react-query';

import { ReactMutationKey } from '@/constants/react-query-key';
import { createChatMessage } from '@/services/chat/create-chat-message';
import { ChatMessageStreamEvent, ChatMessageType, StreamingMessageState } from '@/types/chat';
import { decodeChatStreamChunk } from '@/utils/decode-chat-stream-chunk';

import { useChatStore } from '../stores/use-chat-store';

type ChatMessageRequest = Parameters<typeof createChatMessage>[0];

interface IUseCreateChatMessageProps {
  chatSessionId: ChatMessageRequest['chatSessionId'] | undefined | null;
}

export const useCreateChatMessage = ({ chatSessionId }: IUseCreateChatMessageProps) => {
  const addChatMessage = useChatStore(state => state.addMessage);
  const setStreamState = useChatStore(state => state.setStreamState);
  const setStreamingMessage = useChatStore(state => state.setStreamingMessage);
  const setStreamReader = useChatStore(state => state.setStreamReader);

  return useMutation({
    mutationKey: [ReactMutationKey.CREATE_CHAT_MESSAGE, chatSessionId],
    mutationFn: async (props: ChatMessageRequest) => {
      const stream = await createChatMessage(props);
      const reader = stream.pipeThrough(new TextDecoderStream()).getReader();
      setStreamReader(props.chatSessionId, reader);

      let fullResponse = '';
      let isCompleteMessage = false;

      while (true) {
        const { value, done } = await reader.read();
        if (done) {
          if (!isCompleteMessage) {
            addChatMessage(props.chatSessionId, {
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

          break;
        }

        const { event, data } = decodeChatStreamChunk(value);

        switch (event) {
          case ChatMessageStreamEvent.METADATA:
            addChatMessage(props.chatSessionId, data);
            setStreamState(props.chatSessionId, StreamingMessageState.PENDING);
            break;
          case ChatMessageStreamEvent.DELTA:
            if (!fullResponse) {
              setStreamState(props.chatSessionId, StreamingMessageState.STREAMING);
            }

            const newChunk = data;
            fullResponse += newChunk;
            setStreamingMessage(props.chatSessionId, fullResponse);
            break;
          case ChatMessageStreamEvent.STREAM_COMPLETE:
            const serverChatResponse = {
              ...data,
              message: fullResponse,
            };
            addChatMessage(props.chatSessionId, serverChatResponse);
            setStreamState(props.chatSessionId, StreamingMessageState.IDLE);
            isCompleteMessage = true;
            break;
        }
      }
    },
    onSettled(_, error, variables) {
      setStreamState(variables.chatSessionId, StreamingMessageState.IDLE);
      setStreamReader(variables.chatSessionId, null);
    },
  });
};
