'use client';

import { Loader2 } from 'lucide-react';
import { useSearchParams } from 'next/navigation';

import ChatMessage from '@/components/chat-message/chat-message';
import { QueryParams } from '@/constants/misc';
import { useGetChatSessionDetail } from '@/hooks/chat/use-get-chat-session-detail';
import { useChatStore } from '@/hooks/stores/use-chat-store';

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
      <div className="space-y-4">
        {chatSessionDetail?.chat_messages.map(message => <ChatMessage key={message.id} chatMessage={message} />)}
      </div>

      <StreamingMessage chatSessionId={chatSessionId} />
    </div>
  );
}
