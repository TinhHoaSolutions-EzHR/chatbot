import React, { FC } from 'react';

import { ChatMessage } from '@/components/chat-message/chat-message';
import { useChatStore } from '@/hooks/stores/use-chat-store';

interface INewMessagesProps {
  chatSessionId: string | null;
}

export const NewMessages: FC<INewMessagesProps> = ({ chatSessionId }) => {
  const messages = useChatStore(state => state.chatSession[chatSessionId ?? '']?.messages);

  return (
    <div className="space-y-4">{messages?.map(message => <ChatMessage key={message.id} chatMessage={message} />)}</div>
  );
};
