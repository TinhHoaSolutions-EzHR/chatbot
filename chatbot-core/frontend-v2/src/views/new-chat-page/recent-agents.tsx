import { FC } from 'react';

import { TempChatModelIcon } from '@/components/temp-chat-model-icon';
import { Button } from '@/components/ui/button';
import { useGetRecentAgents } from '@/hooks/agents/use-get-recent-agents';
import { useAgentStore } from '@/hooks/stores/use-agent-store';
import { IAgent } from '@/types/agent';

interface IAgentButtonProps {
  agent: IAgent;
}

const AgentButton: FC<IAgentButtonProps> = ({ agent }) => {
  const { setSelectedAgent } = useAgentStore();

  return (
    <Button
      onClick={() => setSelectedAgent(agent)}
      variant="ghost"
      className="w-36 px-3 py-[2px] rounded-full border border-zinc-400/30 h-8"
    >
      <TempChatModelIcon size={16} />
      <span className="max-w-[120px] truncate font-semibold text-xs">{agent.name}</span>
    </Button>
  );
};

export const RecentAgents = () => {
  const { data: recentAgents } = useGetRecentAgents();

  // No need to have loading state since we have enabled loading for getting
  // selected agent, which is from the same endpoint for recent agents.
  if (!recentAgents) {
    return null;
  }

  // First agent is the selected agent, so we remove it from the list.
  recentAgents.shift();

  return (
    <div className="flex flex-col items-center gap-6">
      <h3 className="text-sm text-black font-medium">Recent agents</h3>
      <div className="flex items-center gap-4">
        {recentAgents.map(agent => (
          <AgentButton key={agent.id} agent={agent} />
        ))}
      </div>
    </div>
  );
};
