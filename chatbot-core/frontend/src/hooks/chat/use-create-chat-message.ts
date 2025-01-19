import { useMutation } from '@tanstack/react-query';
import { useCallback, useState } from 'react';

import { ReactMutationKey } from '@/constants/react-query-key';
import { createChatMessage } from '@/services/chat/create-chat-message';
import { ChatMessageStreamEvent, IChatMessageResponse } from '@/types/chat';
import { decodeChatStreamChunk } from '@/utils/decode-chat-stream-chunk';

type ChatMessageRequest = Parameters<typeof createChatMessage>[0];

export const useCreateChatMessage = () => {
  const [chunk, setChunk] = useState<string>('');
  const [chatMessageRequest, setChatMessageRequest] = useState<IChatMessageResponse | undefined>();
  const [chatMessageResponse, setChatMessageResponse] = useState<IChatMessageResponse | undefined>();

  // Use a callback to flush updates directly to the UI
  const appendChunk = useCallback((newData: string) => {
    setChunk(prev => prev + newData);
  }, []);

  const mutation = useMutation({
    mutationKey: [ReactMutationKey.CREATE_CHAT_MESSAGE],
    mutationFn: async (props: ChatMessageRequest) => {
      const stream = await createChatMessage(props);
      const reader = stream.pipeThrough(new TextDecoderStream()).getReader();
      let fullResponseMessage = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) {
          break;
        }

        const { event, data } = decodeChatStreamChunk(value);

        switch (event) {
          case ChatMessageStreamEvent.METADATA:
            setChatMessageRequest(data);
            break;
          case ChatMessageStreamEvent.DELTA:
            appendChunk(data);
            fullResponseMessage += data;
            break;
          case ChatMessageStreamEvent.STREAM_COMPLETE:
            setChatMessageResponse({ ...data, message: fullResponseMessage });
            break;
        }
      }
    },
  });

  return {
    chunk,
    chatMessageRequest,
    chatMessageResponse,
    mutation,
  };
};
