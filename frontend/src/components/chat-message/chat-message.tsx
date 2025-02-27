import { Loader2 } from 'lucide-react';
import React, { FC, memo } from 'react';
import Markdown from 'react-markdown';
import { Prism, SyntaxHighlighterProps } from 'react-syntax-highlighter';
import { oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';

import { cn } from '@/lib/utils';
import { ChatMessageType, IChatMessageResponse } from '@/types/chat';

import { TempChatModelIcon } from '../temp-chat-model-icon';
import WillRender from '../will-render';
import CopyButton from './copy-button';

const SyntaxHighlighter = Prism as unknown as typeof React.Component<SyntaxHighlighterProps>;

interface IChatMessageProps {
  chatMessage: Partial<IChatMessageResponse>;
  isThinking?: boolean;
  className?: string;
  newChunk?: string;
}

const ChatMessage: FC<IChatMessageProps> = memo(({ chatMessage, isThinking = false, className }) => {
  const chatMessageContent = chatMessage.message;

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
        <WillRender>
          <WillRender.If when={isThinking}>
            <div className="flex items-center gap-1">
              <Loader2 className="animate-spin" size={14} />
              <p>Searching for your question...</p>
            </div>
          </WillRender.If>
          <WillRender.Else>
            <Markdown
              components={{
                code(props) {
                  const { children, className, ...rest } = props;
                  const match = /language-(\w+)/.exec(className || '');
                  return match ? (
                    <div className="relative group">
                      <CopyButton className="absolute right-2 top-2" content={String(children)} />
                      <SyntaxHighlighter
                        {...rest}
                        ref={rest.ref as any}
                        customStyle={{
                          fontSize: 14,
                          borderRadius: '8px',
                          border: '1px solid #e5e5e5',
                        }}
                        PreTag="pre"
                        language={match[1]}
                        style={oneLight}
                      >
                        {String(children).replace(/\n$/, '')}
                      </SyntaxHighlighter>
                    </div>
                  ) : (
                    <code {...rest} className={cn(className, 'code')}>
                      {children}
                    </code>
                  );
                },
              }}
              className={cn(
                'prose prose-sm prose-pre:bg-transparent prose-pre:m-0 prose-pre:p-0 prose-code:before:hidden prose-code:after:hidden prose-stone max-w-full',
                className,
              )}
            >
              {chatMessageContent}
            </Markdown>
          </WillRender.Else>
        </WillRender>
      </div>
    </div>
  );
});
ChatMessage.displayName = 'ChatMessage';

export default ChatMessage;
