import { createContext, FC, ReactNode, useContext, useState } from 'react';

interface IChatSessionContextProps {
  isEditingChatSession: boolean;
  setIsEditingChatSession(isTrue: boolean): void;
  chatSessionDescription: string;
  setChatSessionDescription(description: string): void;
}

export const ChatSessionContext = createContext<IChatSessionContextProps>({
  isEditingChatSession: false,
  setIsEditingChatSession() {},
  chatSessionDescription: '',
  setChatSessionDescription() {},
});

type Props = {
  children: ReactNode;
};

export const ChatSessionProvider: FC<Props> = ({ children }) => {
  const [isEditingChatSession, setIsEditingChatSession] = useState<boolean>(false);
  const [chatSessionDescription, setChatSessionDescription] = useState<string>('');

  return (
    <ChatSessionContext.Provider
      value={{ isEditingChatSession, setIsEditingChatSession, chatSessionDescription, setChatSessionDescription }}
    >
      {children}
    </ChatSessionContext.Provider>
  );
};

export const useChatSessionContext = () => useContext(ChatSessionContext);
