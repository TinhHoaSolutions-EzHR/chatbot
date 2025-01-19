import { createContext, FC, ReactNode, useContext, useState } from 'react';
import { toast } from 'sonner';

import { useEditChatSession } from '@/hooks/chat/use-edit-chat-session';
import { IChatSession } from '@/types/chat';

interface IChatSessionContextProps {
  isEditingChatSession: boolean;
  isPending: boolean;
  setIsEditingChatSession(isTrue: boolean): void;
  chatSessionDescription: string;
  setChatSessionDescription(description: string): void;
  onEditChatSession(): void;
}

export const ChatSessionContext = createContext<IChatSessionContextProps>({
  isEditingChatSession: false,
  isPending: false,
  setIsEditingChatSession() {},
  chatSessionDescription: '',
  setChatSessionDescription() {},
  onEditChatSession() {},
});

type Props = {
  children: ReactNode;
  chatSession: IChatSession;
};

export const ChatSessionProvider: FC<Props> = ({ children, chatSession }) => {
  const [isEditingChatSession, setIsEditingChatSession] = useState<boolean>(false);
  const [chatSessionDescription, setChatSessionDescription] = useState<string>('');

  const { mutate, isPending } = useEditChatSession(true);

  const onEditChatSession = () => {
    if (chatSession.id === chatSessionDescription) {
      setIsEditingChatSession(false);
    }

    mutate(
      {
        chatSessionId: chatSession.id,
        data: {
          description: chatSessionDescription,
        },
      },
      {
        onError() {
          toast.error('Failed to modify chat description.', {
            description: "There's something wrong with your request. Please try again later!",
          });
        },
      },
    );
    setIsEditingChatSession(false);
  };

  return (
    <ChatSessionContext.Provider
      value={{
        isEditingChatSession,
        setIsEditingChatSession,
        chatSessionDescription,
        setChatSessionDescription,
        onEditChatSession,
        isPending,
      }}
    >
      {children}
    </ChatSessionContext.Provider>
  );
};

export const useChatSessionContext = () => useContext(ChatSessionContext);
