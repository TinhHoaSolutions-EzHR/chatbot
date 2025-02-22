import { FC, useEffect } from 'react';

import { SupportedKeys } from '@/constants/misc';
import { cn } from '@/lib/utils';
import { IChatSession } from '@/types/chat';

import { useChatSessionContext } from './chat-session-context';

interface IChatSessionInputProps {
  chatSession: IChatSession;
}

export const ChatSessionInput: FC<IChatSessionInputProps> = ({ chatSession }) => {
  const {
    isEditingChatSession,
    setIsEditingChatSession,
    chatSessionDescription,
    setChatSessionDescription,
    onEditChatSession,
    isPending,
  } = useChatSessionContext();

  useEffect(() => {
    if (isEditingChatSession) {
      setChatSessionDescription(chatSession.description ?? chatSession.id);
    }
  }, [isEditingChatSession]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === SupportedKeys.ESCAPE) {
      setIsEditingChatSession(false);
      return;
    }

    if (e.key === SupportedKeys.ENTER) {
      onEditChatSession();
    }
  };

  if (isEditingChatSession) {
    return (
      <input
        className={cn(
          'w-32 border border-solid border-zinc-200 rounded p-[2px] cursor-text',
          !!isPending && 'pointer-events-none',
        )}
        value={chatSessionDescription}
        onChange={e => setChatSessionDescription(e.target.value)}
        onKeyDown={handleKeyDown}
        autoFocus
      />
    );
  }

  return <>{chatSession.description ?? chatSession.id}</>;
};
