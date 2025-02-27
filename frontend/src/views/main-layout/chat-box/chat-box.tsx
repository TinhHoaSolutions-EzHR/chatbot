'use client';

import { useIsMutating } from '@tanstack/react-query';
import { ArrowUpIcon, PlusCircle, Search, Square } from 'lucide-react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useState } from 'react';

import { Button } from '@/components/ui/button';
import WillRender from '@/components/will-render';
import { QueryParams, Route, SupportedKeys } from '@/constants/misc';
import { ReactMutationKey } from '@/constants/react-query-key';
import { useNewChatHelper } from '@/hooks/chat/use-new-chat-helper';
import { useChatStore } from '@/hooks/stores/use-chat-store';
import { useGetUserInfo } from '@/hooks/user/use-get-user-info';
import { ChatMessageRequestType } from '@/types/chat';
import { UserRole } from '@/types/user';

import { AutoHeightTextarea } from './auto-height-textarea/auto-height-textarea';

export const ChatBox = () => {
  const { data: userInfo } = useGetUserInfo();
  const router = useRouter();

  const [userInput, setUserInput] = useState<string>('');
  const searchParams = useSearchParams();
  const chatSessionId = searchParams.get(QueryParams.CHAT_SESSION_ID);

  const isCreatingMessage = useIsMutating({
    mutationKey: [ReactMutationKey.CREATE_CHAT_MESSAGE, chatSessionId],
  });

  const createNewChat = useNewChatHelper({
    chatSessionId,
    disabled: !!isCreatingMessage,
    chatRequestType: ChatMessageRequestType.NEW,
  });
  const cancelStream = useChatStore(state => state.cancelStream);

  const onButtonClick = async () => {
    if (!isCreatingMessage) {
      await createNewChat(userInput);
      setUserInput('');
      return;
    }

    if (chatSessionId) {
      cancelStream(chatSessionId);
    }
  };

  return (
    <div className="chat-width mb-8 relative border border-[#e5e7eb] rounded-lg bg-[#f5f5f5] overflow-hidden">
      <AutoHeightTextarea
        className="w-full text-[#262626] placeholder:text-[#666666] bg-[#f5f5f5]"
        value={userInput}
        onChange={e => setUserInput(e.target.value)}
        onKeyDown={async e => {
          if (e.key === SupportedKeys.ENTER) {
            await createNewChat(userInput);
            setUserInput('');
          }
        }}
        placeholder="Chat something..."
      />
      <div className="px-4 pb-2 flex items-center gap-3">
        <WillRender when={userInfo?.role === UserRole.ADMIN}>
          <Button
            size="sm"
            variant="ghost"
            className="p-[6px] hover:bg-zinc-400/15"
            onClick={() => router.push(Route.ADD_FILE_CONNECTOR)}
          >
            <PlusCircle size={14} />
            <p className="text-sm">File</p>
          </Button>
        </WillRender>
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
