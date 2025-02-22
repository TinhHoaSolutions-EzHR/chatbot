import React, { FC } from 'react';

import { ChatMessage } from '@/components/chat-message/chat-message';
import { IChatSessionDetail } from '@/types/chat';

interface IPreviousMessagesProps {
  chatSessionDetail: IChatSessionDetail | undefined;
}

export const PreviousMessages: FC<IPreviousMessagesProps> = ({ chatSessionDetail }) => {
  return (
    <div className="space-y-4">
      {chatSessionDetail?.chat_messages.map(message => <ChatMessage key={message.id} chatMessage={message} />)}
    </div>
  );
};
