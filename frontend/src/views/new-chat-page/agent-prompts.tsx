import { FC } from 'react';

import { Skeleton } from '@/components/ui/skeleton';
import { useGetAgentDetail } from '@/hooks/agents/use-get-agent-detail';
import { useNewChatHelper } from '@/hooks/chat/use-new-chat-helper';

interface IAgentPromptsProps {
  agentId: string;
}

export const AgentPrompts: FC<IAgentPromptsProps> = ({ agentId }) => {
  const { data: agent, isPending } = useGetAgentDetail(agentId);
  const { onNewChat } = useNewChatHelper();

  if (isPending) {
    return (
      <div className="grid grid-cols-4 gap-6">
        {Array.from({ length: 4 }).map((_, index) => (
          <Skeleton key={index} className="w-full rounded-2xl h-24 px-3 py-2" />
        ))}
      </div>
    );
  }

  const shownStarterMessages = agent?.starter_messages.slice(0, 4);

  if (!shownStarterMessages || shownStarterMessages.length === 0) {
    return null;
  }

  return (
    <div className="grid grid-cols-4 gap-6">
      {shownStarterMessages.length < 4 && <div />}
      {shownStarterMessages.map(starterMessage => (
        <div
          key={`${starterMessage.id}`}
          className="w-full rounded-2xl px-3 py-2 justify-normal items-start h-24 border border-solid border-zinc-400/30 cursor-pointer hover:bg-zinc-200/30 transition"
          onClick={() => onNewChat(starterMessage.message)}
        >
          <p className="line-clamp-3 h-full flex">{starterMessage.name}</p>
        </div>
      ))}
      {shownStarterMessages.length < 4 && <div />}
    </div>
  );
};
