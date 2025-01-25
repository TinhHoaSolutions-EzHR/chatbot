import { useMutation } from '@tanstack/react-query';
import { useRef, useState } from 'react';

import { ReactMutationKey } from '@/constants/react-query-key';
import { createChatMessage } from '@/services/chat/create-chat-message';
import { ChatMessageStreamEvent, IChatMessageResponse, StreamingMessageState } from '@/types/chat';
import { decodeChatStreamChunk } from '@/utils/decode-chat-stream-chunk';

type ChatMessageRequest = Parameters<typeof createChatMessage>[0];

interface IUseCreateChatMessageProps {
  chatSessionId: ChatMessageRequest['chatSessionId'] | undefined | null;
  changeStreamState?: (state: StreamingMessageState) => void;
  addChatMessage?: (message: IChatMessageResponse) => void;
}

export const useCreateChatMessage = ({
  chatSessionId,
  changeStreamState,
  addChatMessage,
}: IUseCreateChatMessageProps) => {
  const [chunk, setChunk] = useState<string>('');
  const fullResponseRef = useRef<string>('');

  const mutation = useMutation({
    mutationKey: [ReactMutationKey.CREATE_CHAT_MESSAGE, chatSessionId],
    mutationFn: async (props: ChatMessageRequest) => {
      const stream = await createChatMessage(props);
      const reader = stream.pipeThrough(new TextDecoderStream()).getReader();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const { event, data } = decodeChatStreamChunk(value);

        switch (event) {
          case ChatMessageStreamEvent.METADATA:
            addChatMessage?.(data);
            changeStreamState?.(StreamingMessageState.PENDING);
            break;
          case ChatMessageStreamEvent.DELTA:
            if (fullResponseRef.current.length === 0) {
              changeStreamState?.(StreamingMessageState.STREAMING);
            }

            const newChunk = data;
            fullResponseRef.current += newChunk;
            setChunk(fullResponseRef.current);
            break;
          case ChatMessageStreamEvent.STREAM_COMPLETE:
            const serverChatResponse = {
              ...data,
              message: fullResponseRef.current,
            };
            addChatMessage?.(serverChatResponse);
            changeStreamState?.(StreamingMessageState.IDLE);
            fullResponseRef.current = '';
            setChunk('');
            break;
        }
      }
    },
    onSettled() {
      changeStreamState?.(StreamingMessageState.IDLE);
    },
  });

  return {
    chunk,
    mutation,
  };
};
