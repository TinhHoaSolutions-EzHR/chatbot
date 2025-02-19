'use client';

import { Loader2 } from 'lucide-react';
import { useSearchParams } from 'next/navigation';

import { QueryParams } from '@/constants/misc';
import { useGetChatSessionDetail } from '@/hooks/chat/use-get-chat-session-detail';
import { useChatStore } from '@/hooks/stores/use-chat-store';

import { NewChatHandler } from './new-chat-handler';
import { NewMessages } from './new-messages';
import { PreviousMessages } from './previous-messages';
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
    <div className="chat-width h-full space-y-4 pb-8">
      <NewChatHandler />
      <PreviousMessages chatSessionDetail={chatSessionDetail} />
      <NewMessages chatSessionId={chatSessionId} />
      <StreamingMessage chatSessionId={chatSessionId} />
    </div>
  );
}
