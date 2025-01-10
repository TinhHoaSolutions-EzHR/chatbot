import { FC, useMemo } from 'react';
import { toast } from 'sonner';

import { TempChatModelIcon } from '@/components/temp-chat-model-icon';
import { Button } from '@/components/ui/button';
import { useGetAgentsList } from '@/hooks/agents/use-get-agents-list';
import { useSelectAgent } from '@/hooks/agents/use-select-agent';
import { useAgentStore } from '@/hooks/stores/use-agent-store';
import { useGetUserSettings } from '@/hooks/user/use-get-user-settings';
import { IAgent } from '@/types/agent';

interface IAgentButtonProps {
  agent: IAgent;
}

const AgentButton: FC<IAgentButtonProps> = ({ agent }) => {
  const { mutate } = useSelectAgent();
  const { setSelectedAgent, selectedAgent } = useAgentStore();

  return (
    <Button
      onClick={() => {
        if (selectedAgent?.id === agent.id) {
          return;
        }

        setSelectedAgent(agent);
        mutate(agent.id, {
          onError() {
            toast.error('Select agent error', {
              description: "There's something wrong with your request, please try again later",
            });
            setSelectedAgent(null);
          },
        });
      }}
      variant="ghost"
      className="w-36 px-3 py-[2px] rounded-full border border-zinc-400/30 h-8"
    >
      <TempChatModelIcon size={16} />
      <span className="max-w-[120px] truncate font-semibold text-xs">{agent.name}</span>
    </Button>
  );
};

export const RecentAgents = () => {
  const { data: userSettings } = useGetUserSettings();
  const { mappedAgentsById } = useGetAgentsList().data ?? {};

  const recentAgents = useMemo(() => {
    if (!userSettings?.recent_agent_ids || !mappedAgentsById) {
      return undefined;
    }

    const agentsList = userSettings.recent_agent_ids.reduce<IAgent[]>((acc, cur) => {
      if (mappedAgentsById[cur]) {
        acc.push(mappedAgentsById[cur]);
      }

      return acc;
    }, []);

    agentsList.shift();
    return agentsList;
  }, [userSettings, mappedAgentsById]);

  // No need to have loading state since we have enabled loading for getting
  // selected agent, which is from the same endpoint for recent agents.
  if (!recentAgents) {
    return null;
  }

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
