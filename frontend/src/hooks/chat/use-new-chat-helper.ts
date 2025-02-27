import { useRouter } from 'next/navigation';
import { toast } from 'sonner';

import { QueryParams, Route } from '@/constants/misc';
import { useGetSelectedAgent } from '@/hooks/agents/use-get-selected-agent';
import { useCreateChatSession } from '@/hooks/chat/use-create-chat-session';
import { ChatMessageRequestType } from '@/types/chat';
import ToastService from '@/utils/default-toasts';

import { useCreateChatMessage } from './use-create-chat-message';

interface INewChatHelperProps {
  chatSessionId: string | null;
  disabled?: boolean;
  chatRequestType: ChatMessageRequestType;
}

export const useNewChatHelper = (props?: INewChatHelperProps) => {
  const { disabled, chatSessionId, chatRequestType } = props || {};
  const router = useRouter();

  const selectedAgent = useGetSelectedAgent();

  const { mutateAsync: createChatSession } = useCreateChatSession();
  const { mutate: createChatMessage } = useCreateChatMessage({ chatSessionId });

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

      // User creating a new chat
      const chatSession = await createChatSession(selectedAgent.id, {
        onError() {
          ToastService.apiFail();
        },
      });

      createNewChat(chatSession.id);
      router.push(`${Route.CHAT}/?${QueryParams.CHAT_SESSION_ID}=${chatSession.id}`);

      return;
    }

    createNewChat(chatSessionId);

    function createNewChat(chatSessionId: string) {
      createChatMessage({
        chatSessionId,
        data: {
          message: userInput,
          chat_message_request_type: chatRequestType,
        },
      });
    }
  };

  return onNewChat;
};
