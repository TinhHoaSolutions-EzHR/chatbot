'use client';

import { ArrowUpIcon, PlusCircle, Search } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { QueryParams, Route, SupportedKeys } from '@/constants/misc';
import { useGetSelectedAgent } from '@/hooks/agents/use-get-selected-agent';
import { useCreateChatSession } from '@/hooks/chat/use-create-chat-session';

import { AutoHeightTextarea } from './auto-height-textarea/auto-height-textarea';

export const ChatBox = () => {
  const router = useRouter();
  const [prompt, setPrompt] = useState('');
  const { mutate } = useCreateChatSession();

  const selectedAgent = useGetSelectedAgent();

  return (
    <div className="chat-width mb-8 relative border border-[#e5e7eb] rounded-lg bg-[#f5f5f5] overflow-hidden">
      <AutoHeightTextarea
        className="w-full text-[#262626] placeholder:text-[#666666] bg-[#f5f5f5]"
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
        onKeyDown={e =>
          (e.altKey || e.metaKey) &&
          e.key === SupportedKeys.ENTER &&
          selectedAgent &&
          mutate(selectedAgent.id, {
            onSuccess(data) {
              router.push(`${Route.CHAT}?${QueryParams.CHAT_SESSION_ID}=${data.id}`);
            },
            onError() {
              toast.error('Something went wrong.', {
                description: 'Please try again later',
              });
            },
          })
        }
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
      <Button className="absolute right-4 bottom-4 rounded-full w-fit h-fit p-1 m-0" disabled={prompt.length === 0}>
        <ArrowUpIcon size={20} />
      </Button>
    </div>
  );
};
