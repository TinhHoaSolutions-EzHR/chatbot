import React, { FC } from 'react';

import { ChatMessage } from '@/components/chat-message/chat-message';
import WillRender from '@/components/will-render';
import { useStreamingChatContext } from '@/providers/streaming-chat-provider';
import { ChatMessageType, StreamingMessageState } from '@/types/chat';

export const StreamingMessage: FC = () => {
  const { streamingMessage, streamState } = useStreamingChatContext();

  return (
    <WillRender when={streamState !== StreamingMessageState.IDLE}>
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
