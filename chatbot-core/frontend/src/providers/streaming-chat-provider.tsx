import { useSearchParams } from 'next/navigation';
import { createContext, ReactNode, useContext, useEffect, useRef, useState } from 'react';

import { QueryParams } from '@/constants/misc';
import { useCreateChatMessage } from '@/hooks/chat/use-create-chat-message';
import { useChatStore } from '@/hooks/stores/use-chat-store';
import { ChatMessageRequestType, StreamingMessageState } from '@/types/chat';

import { useNewChatsContext } from './new-chats-provider';

interface IStreamingChatContext {
  streamingMessage: string;
  streamState: StreamingMessageState;
}

const StreamingChatContext = createContext<IStreamingChatContext>({
  streamingMessage: '',
  streamState: StreamingMessageState.IDLE,
});

type Props = {
  children: ReactNode;
};

export default function StreamingChatProvider({ children }: Props) {
  const searchParams = useSearchParams();
  const chatSessionId = searchParams.get(QueryParams.CHAT_SESSION_ID);

  const [streamState, setStreamState] = useState<StreamingMessageState>(StreamingMessageState.IDLE);

  const { addMessage } = useNewChatsContext();

  const {
    chunk,
    mutation: { mutate },
  } = useCreateChatMessage({
    chatSessionId,
    addChatMessage: addMessage,
    changeStreamState: setStreamState,
  });

  const { userMessage, clearChatStore } = useChatStore();

  const shouldTriggerRef = useRef<boolean>(true);

  useEffect(() => {
    if (!userMessage || !chatSessionId || !shouldTriggerRef.current) {
      return;
    }

    shouldTriggerRef.current = false;

    mutate(
      {
        chatSessionId,
        data: {
          chat_message_request_type: ChatMessageRequestType.NEW,
          message: userMessage,
        },
      },
      {
        onSettled() {
          shouldTriggerRef.current = true;
        },
      },
    );

    clearChatStore();
  }, [userMessage, chatSessionId]);

  return (
    <StreamingChatContext.Provider value={{ streamingMessage: chunk, streamState }}>
      {children}
    </StreamingChatContext.Provider>
  );
}

export const useStreamingChatContext = () => useContext(StreamingChatContext);
