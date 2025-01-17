import { useRouter, useSearchParams } from 'next/navigation';
import { toast } from 'sonner';

import { QueryParams, Route } from '@/constants/misc';
import { useGetSelectedAgent } from '@/hooks/agents/use-get-selected-agent';
import { useCreateChatSession } from '@/hooks/chat/use-create-chat-session';
import { useChatStore } from '@/hooks/stores/use-chat-store';

export const useNewChatHelper = (clearUserInput: () => void) => {
  const router = useRouter();

  const setMessage = useChatStore(state => state.setMessage);
  const setIsNewMessage = useChatStore(state => state.setIsNewMessage);
  const setChatSessionId = useChatStore(state => state.setChatSessionId);

  const searchParams = useSearchParams();
  const chatSessionId = searchParams.get(QueryParams.CHAT_SESSION_ID);

  const selectedAgent = useGetSelectedAgent();

  const { mutate } = useCreateChatSession();

  const updateNewChat = (userInput: string, chatSessionId: string) => {
    setMessage(userInput);
    setIsNewMessage(true);
    setChatSessionId(chatSessionId);
  };

  const onNewChat = async (userInput: string) => {
    if (!userInput) {
      toast.error('Please enter your input first.');
      return;
    }

    // Case when user on the home page and create a new chat message
    if (!chatSessionId) {
      if (!selectedAgent) {
        return;
      }

      mutate(selectedAgent.id, {
        onSuccess(newChatSession) {
          updateNewChat(userInput, newChatSession.id);
          clearUserInput();
          router.push(`${Route.CHAT}/?${QueryParams.CHAT_SESSION_ID}=${newChatSession.id}`);
        },
        onError() {
          toast.error('Something went wrong', {
            description: "There's something wrong with your request. Please try again later.",
          });
        },
      });

      return;
    }

    // Case when user is in a chat session
    updateNewChat(userInput, chatSessionId);
    clearUserInput();
  };

  return {
    onNewChat,
  };
};
