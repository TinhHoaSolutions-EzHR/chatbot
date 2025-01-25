import { createContext, ReactNode, useCallback, useContext, useState } from 'react';

import { IChatMessageResponse } from '@/types/chat';

interface INewChatsContext {
  messages: IChatMessageResponse[];
  addMessage(message: IChatMessageResponse): void;
}

const NewChatsContext = createContext<INewChatsContext>({
  messages: [],
  addMessage() {},
});

type Props = {
  children: ReactNode;
};

export default function NewChatsProvider({ children }: Props) {
  const [messages, setMessages] = useState<IChatMessageResponse[]>([]);

  const addMessage = useCallback((message: IChatMessageResponse) => {
    setMessages(prevState => [...prevState, message]);
  }, []);

  return <NewChatsContext.Provider value={{ messages, addMessage }}>{children}</NewChatsContext.Provider>;
}

export const useNewChatsContext = () => useContext(NewChatsContext);
