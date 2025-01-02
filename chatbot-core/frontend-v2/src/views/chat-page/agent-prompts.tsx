import { FC } from 'react';

import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { useGetAgent } from '@/hooks/agents/use-get-agent';

interface IAgentPromptsProps {
  agentId: string;
}

export const AgentPrompts: FC<IAgentPromptsProps> = ({ agentId }) => {
  const { data: agentWithPrompts, isPending } = useGetAgent(agentId);

  if (isPending) {
    return (
      <div className="grid grid-cols-4 gap-6">
        {Array.from({ length: 4 }).map((_, index) => (
          <Skeleton key={index} className="w-full rounded-2xl h-[5.2rem] px-3 py-2" />
        ))}
      </div>
    );
  }

  const shownPrompts = agentWithPrompts?.prompts.slice(0, 4);

  if (!shownPrompts || shownPrompts.length === 0) {
    return null;
  }

  return (
    <div className="grid grid-cols-4 gap-6">
      {shownPrompts.length < 4 && <div />}
      {shownPrompts.map(prompt => (
        <Button
          key={prompt.id}
          variant="ghost"
          className="w-full rounded-2xl px-3 py-2 justify-normal items-start h-[5.2rem] line-clamp-3 flex border border-solid border-zinc-400/30"
        >
          {prompt.name}
        </Button>
      ))}
      {shownPrompts.length < 4 && <div />}
    </div>
  );
};
