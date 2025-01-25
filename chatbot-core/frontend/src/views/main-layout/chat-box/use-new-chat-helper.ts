import { useRouter } from 'next/navigation';
import { toast } from 'sonner';

import { QueryParams, Route } from '@/constants/misc';
import { useGetSelectedAgent } from '@/hooks/agents/use-get-selected-agent';
import { useCreateChatSession } from '@/hooks/chat/use-create-chat-session';
import { useChatStore } from '@/hooks/stores/use-chat-store';

interface INewChatHelperProps {
  chatSessionId: string | null;
  disabled?: boolean;
  onSuccess(): void;
}

export const useNewChatHelper = ({ disabled, onSuccess, chatSessionId }: INewChatHelperProps) => {
  const router = useRouter();

  const setUserMessage = useChatStore(state => state.setUserMessage);
  const setIsNewChat = useChatStore(state => state.setIsNewChat);

  const selectedAgent = useGetSelectedAgent();

  const { mutate } = useCreateChatSession();

  const updateNewChat = (userInput: string, isNewChat: boolean) => {
    setUserMessage(userInput);
    setIsNewChat(isNewChat);
  };

  const onNewChat = async (userInput: string) => {
    if (disabled) {
      return;
    }

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
          // User creating a new chat
          updateNewChat(userInput, true);
          onSuccess();
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
    updateNewChat(userInput, false);
    onSuccess();
  };

  return {
    onNewChat,
  };
};
