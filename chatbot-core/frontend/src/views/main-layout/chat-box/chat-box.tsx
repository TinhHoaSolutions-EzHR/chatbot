'use client';

import { useIsMutating } from '@tanstack/react-query';
import { ArrowUpIcon, PlusCircle, Search, Square } from 'lucide-react';
import { useSearchParams } from 'next/navigation';
import { useState } from 'react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { QueryParams, SupportedKeys } from '@/constants/misc';
import { ReactMutationKey } from '@/constants/react-query-key';
import { useNewChatHelper } from '@/hooks/chat/use-new-chat-helper';

import { AutoHeightTextarea } from './auto-height-textarea/auto-height-textarea';

export const ChatBox = () => {
  const [userInput, setUserInput] = useState<string>('');
  const searchParams = useSearchParams();
  const chatSessionId = searchParams.get(QueryParams.CHAT_SESSION_ID);

  const isCreatingMessage = useIsMutating({
    mutationKey: [ReactMutationKey.CREATE_CHAT_MESSAGE, chatSessionId],
  });

  const { onNewChat } = useNewChatHelper({
    chatSessionId,
    onSuccess() {
      setUserInput('');
    },
    disabled: !!isCreatingMessage,
  });

  const onButtonClick = () => {
    if (!isCreatingMessage) {
      onNewChat(userInput);
      return;
    }

    // Implement aborting chat here
    toast.info('This feature will be supported in the future.');
  };

  return (
    <div className="chat-width mb-8 relative border border-[#e5e7eb] rounded-lg bg-[#f5f5f5] overflow-hidden">
      <AutoHeightTextarea
        className="w-full text-[#262626] placeholder:text-[#666666] bg-[#f5f5f5]"
        value={userInput}
        onChange={e => setUserInput(e.target.value)}
        onKeyDown={e => (e.ctrlKey || e.metaKey) && e.key === SupportedKeys.ENTER && onNewChat(userInput)}
        placeholder="Chat something..."
      />
      <div className="px-4 pb-2 flex items-center gap-3">
        <Button size="sm" variant="ghost" className="p-[6px] hover:bg-zinc-400/15">
          <PlusCircle size={14} />
          <p className="text-sm">File</p>
        </Button>
        <Button size="sm" variant="ghost" className="p-[6px] hover:bg-zinc-400/15">
          <Search size={14} />
          <p className="text-sm">Filters</p>
        </Button>
      </div>
      <Button
        className="absolute right-4 bottom-4 rounded-full m-0 p-0 h-8 w-8"
        disabled={!userInput && !isCreatingMessage}
        onClick={onButtonClick}
      >
        {!!isCreatingMessage ? <Square size={16} fill="#fff" /> : <ArrowUpIcon size={20} />}
      </Button>
    </div>
  );
};
