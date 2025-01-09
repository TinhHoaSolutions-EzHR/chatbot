import { FC } from 'react';

import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { useGetAgentDetail } from '@/hooks/agents/use-get-agent-detail';

interface IAgentPromptsProps {
  agentId: string;
}

export const AgentPrompts: FC<IAgentPromptsProps> = ({ agentId }) => {
  const { data: agent, isPending } = useGetAgentDetail(agentId);

  if (isPending) {
    return (
      <div className="grid grid-cols-4 gap-6">
        {Array.from({ length: 4 }).map((_, index) => (
          <Skeleton key={index} className="w-full rounded-2xl h-[5.2rem] px-3 py-2" />
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
      {shownStarterMessages.map((starterMessage, idx) => (
        <Button
          key={`${starterMessage}-${idx}`}
          variant="ghost"
          className="w-full rounded-2xl px-3 py-2 justify-normal items-start h-[5.2rem] line-clamp-3 flex border border-solid border-zinc-400/30"
        >
          {starterMessage}
        </Button>
      ))}
      {shownStarterMessages.length < 4 && <div />}
    </div>
  );
};
