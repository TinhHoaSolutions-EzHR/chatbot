import { FC, useEffect } from 'react';

import { SupportedKeys } from '@/constants/misc';
import { cn } from '@/lib/utils';
import { IChatSession } from '@/types/chat';

import { useChatSessionContext } from './chat-session-context';

interface IChatSessionInputProps {
  chatSession: IChatSession;
  onEditChatSession(): void;
  isPending: boolean;
}

export const ChatSessionInput: FC<IChatSessionInputProps> = ({ chatSession, onEditChatSession, isPending }) => {
  const { isEditingChatSession, chatSessionDescription, setChatSessionDescription } = useChatSessionContext();

  useEffect(() => {
    if (isEditingChatSession) {
      setChatSessionDescription(chatSession.description ?? chatSession.id);
    }
  }, [isEditingChatSession]);

  if (isEditingChatSession) {
    return (
      <input
        className={cn(
          'w-32 border border-solid border-zinc-200 rounded p-[2px] cursor-text',
          !!isPending && 'pointer-events-none',
        )}
        value={chatSessionDescription}
        onChange={e => setChatSessionDescription(e.target.value)}
        onKeyDown={e => e.key === SupportedKeys.ENTER && onEditChatSession()}
        autoFocus
      />
    );
  }

  return <>{chatSession.description ?? chatSession.id}</>;
};
