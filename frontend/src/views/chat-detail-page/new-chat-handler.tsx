'use client';

import { useSearchParams } from 'next/navigation';
import { FC, useEffect } from 'react';

import { QueryParams } from '@/constants/misc';
import { useCreateChatMessage } from '@/hooks/chat/use-create-chat-message';
import { useChatStore } from '@/hooks/stores/use-chat-store';
import { ChatMessageRequestType } from '@/types/chat';

export const NewChatHandler: FC = () => {
  const searchParams = useSearchParams();
  const chatSessionId = searchParams.get(QueryParams.CHAT_SESSION_ID);

  const { mutate } = useCreateChatMessage({
    chatSessionId,
  });

  const userMessage = useChatStore(state => state.userMessage);
  const clearUserNewChat = useChatStore(state => state.clearUserNewChat);
  const initChatSessionIfNotExist = useChatStore(state => state.initChatSessionIfNotExist);

  useEffect(() => {
    if (!chatSessionId) {
      return;
    }

    initChatSessionIfNotExist(chatSessionId);
  }, [chatSessionId]);

  useEffect(() => {
    if (!userMessage || !chatSessionId) {
      return;
    }

    mutate({
      chatSessionId,
      data: {
        chat_message_request_type: ChatMessageRequestType.NEW,
        message: userMessage,
      },
    });

    clearUserNewChat();
  }, [userMessage, chatSessionId]);

  return null;
};
