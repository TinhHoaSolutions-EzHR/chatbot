'use client';

import { Loader2 } from 'lucide-react';
import { useSearchParams } from 'next/navigation';

import { QueryParams } from '@/constants/misc';
import { useGetChatSessionDetail } from '@/hooks/chat/use-get-chat-session-detail';
import { useChatStore } from '@/hooks/stores/use-chat-store';

import { NewMessages } from './new-messages';
import { PreviousMessages } from './previous-messages';
import NewChatsProvider from './providers/new-chats-provider';
import StreamingChatProvider from './providers/streaming-chat-provider';
import { StreamingMessage } from './streaming-message';

export default function ChatDetailPage() {
  const searchParams = useSearchParams();
  const chatSessionId = searchParams.get(QueryParams.CHAT_SESSION_ID);

  const isNewChat = useChatStore(state => state.isNewChat);

  const { data: chatSessionDetail, isPending: isLoadingChatSessionDetail } = useGetChatSessionDetail(chatSessionId);

  if (isLoadingChatSessionDetail && !isNewChat) {
    return (
      <div className="chat-width h-full grid place-items-center">
        <Loader2 className="animate-spin" size={32} />
      </div>
    );
  }

  return (
    <NewChatsProvider>
      <StreamingChatProvider>
        <div className="chat-width h-full space-y-4 pb-8">
          <PreviousMessages chatSessionDetail={chatSessionDetail} />
          <NewMessages />
          <StreamingMessage />
        </div>
      </StreamingChatProvider>
    </NewChatsProvider>
  );
}
