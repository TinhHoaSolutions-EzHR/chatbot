import { useMutation } from '@tanstack/react-query';

import { ReactMutationKey } from '@/constants/react-query-key';
import { createChatMessage } from '@/services/chat/create-chat-message';
import { ChatMessageStreamEvent, StreamingMessageState } from '@/types/chat';
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

  return useMutation({
    mutationKey: [ReactMutationKey.CREATE_CHAT_MESSAGE, chatSessionId],
    mutationFn: async (props: ChatMessageRequest) => {
      const stream = await createChatMessage(props);
      const reader = stream.pipeThrough(new TextDecoderStream()).getReader();

      let fullResponse = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

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
            break;
        }
      }
    },
    onSettled(_, __, variables) {
      setStreamState(variables.chatSessionId, StreamingMessageState.IDLE);
    },
  });
};
