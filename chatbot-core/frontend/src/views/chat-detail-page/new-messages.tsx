import React, { FC } from 'react';

import { ChatMessage } from '@/components/chat-message/chat-message';

import { useNewChatsContext } from './providers/new-chats-provider';

export const NewMessages: FC = () => {
  const { messages } = useNewChatsContext();

  return (
    <div className="space-y-4">
      {messages.map(message => (
        <ChatMessage key={message.id} chatMessage={message} />
      ))}
    </div>
  );
};
