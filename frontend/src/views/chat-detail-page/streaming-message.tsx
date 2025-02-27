import React, { FC } from 'react';

import ChatMessage from '@/components/chat-message/chat-message';
import WillRender from '@/components/will-render';
import { useChatStore } from '@/hooks/stores/use-chat-store';
import { ChatMessageType, StreamingMessageState } from '@/types/chat';

interface IStreamingMessageProps {
  chatSessionId: string | null;
}

export const StreamingMessage: FC<IStreamingMessageProps> = ({ chatSessionId }) => {
  const streamingMessage = useChatStore(state => state.chatSession[chatSessionId ?? '']?.streamingMessage) ?? '';
  const streamState = useChatStore(state => state.chatSession[chatSessionId ?? '']?.streamState);

  return (
    <WillRender when={!!streamState && streamState !== StreamingMessageState.IDLE}>
      <ChatMessage
        isThinking={streamState === StreamingMessageState.PENDING}
        chatMessage={{
          message_type: ChatMessageType.ASSISTANT,
          message: streamingMessage,
        }}
      />
    </WillRender>
  );
};
