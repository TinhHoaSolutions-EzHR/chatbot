import { FC, useEffect, useState } from 'react';
import { remark } from 'remark';
import html from 'remark-html';

import { cn } from '@/lib/utils';
import { ChatMessageType, IChatMessageResponse } from '@/types/chat';

import { TempChatModelIcon } from '../temp-chat-model-icon';
import WillRender from '../will-render';

import './chat-message.css';

interface IChatMessageProps {
  chatMessage: Partial<IChatMessageResponse>;
  isThinking?: boolean;
}

export const ChatMessage: FC<IChatMessageProps> = ({ chatMessage, isThinking = false }) => {
  const chatMessageContent = chatMessage.message;
  const [processedMessage, setProcessedMessage] = useState<string>('');

  useEffect(() => {
    if (!chatMessageContent) {
      return;
    }

    remark()
      .use(html, {
        allowDangerousHtml: true,
      })
      .process(chatMessageContent)
      .then(res => setProcessedMessage(res.toString()));
  }, [chatMessageContent]);

  return (
    <div
      className={cn(
        'w-full flex relative',
        chatMessage.message_type === ChatMessageType.USER ? 'justify-end' : 'justify-start',
      )}
    >
      <WillRender when={chatMessage.message_type !== ChatMessageType.USER}>
        <div className="p-2 rounded-full border border-zinc-300 border-dashed absolute -left-8 top-1">
          <TempChatModelIcon />
        </div>
      </WillRender>
      <div
        className={cn(
          'rounded-3xl px-4 py-2',
          chatMessage.message_type === ChatMessageType.USER ? 'bg-zinc-200/40 max-w-2xl' : 'w-full',
        )}
      >
        <WillRender when={isThinking}>
          <p>Searching for your question...</p>
        </WillRender>
        <WillRender when={!isThinking}>
          {chatMessage.message_type === ChatMessageType.USER ? (
            chatMessageContent
          ) : (
            <article className="markdown-body" dangerouslySetInnerHTML={{ __html: processedMessage }} />
          )}
        </WillRender>
      </div>
    </div>
  );
};
