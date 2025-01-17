'use client';

import { ArrowUpIcon, PlusCircle, Search } from 'lucide-react';
import { useState } from 'react';

import { Button } from '@/components/ui/button';
import { SupportedKeys } from '@/constants/misc';

import { AutoHeightTextarea } from './auto-height-textarea/auto-height-textarea';
import { useNewChatHelper } from './use-new-chat-helper';

export const ChatBox = () => {
  const [userInput, setUserInput] = useState<string>('');

  const { onNewChat } = useNewChatHelper(() => setUserInput(''));

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
        className="absolute right-4 bottom-4 rounded-full w-fit h-fit p-1 m-0"
        disabled={!userInput}
        onClick={() => onNewChat(userInput)}
      >
        <ArrowUpIcon size={20} />
      </Button>
    </div>
  );
};
