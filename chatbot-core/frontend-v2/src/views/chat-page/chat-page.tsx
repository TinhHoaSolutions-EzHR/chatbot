import { ChatBox } from './chat-box/chat-box';
import { NewChat } from './new-chat';

export default function ChatPage() {
  return (
    <div className="relative w-full flex-1 flex flex-col">
      <div className="absolute inset-0 bottom-[130px] overflow-auto grid place-items-center">
        <NewChat />
      </div>
      <div className="absolute bottom-0 left-0 right-0 flex justify-center px-4">
        <ChatBox />
      </div>
    </div>
  );
}
