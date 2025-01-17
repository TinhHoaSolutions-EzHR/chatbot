import { Check, X } from 'lucide-react';
import { FC } from 'react';

import { cn } from '@/lib/utils';

import { useChatSessionContext } from '../chat-session-context';

export const EditChatSessionButtons: FC = () => {
  const { onEditChatSession, setIsEditingChatSession, isPending } = useChatSessionContext();

  return (
    <div className={cn('absolute top-0 bottom-0 right-2 gap-2 items-center group-hover/folder:flex flex')}>
      <Check size={14} className="text-muted-foreground hover:text-zinc-800" onClick={onEditChatSession} />
      <X
        size={14}
        className="text-muted-foreground hover:text-zinc-800"
        onClick={() => !isPending && setIsEditingChatSession(false)}
      />
    </div>
  );
};
