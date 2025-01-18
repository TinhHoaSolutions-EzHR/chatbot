import { useAgentStore } from '../stores/use-agent-store';
import { useGetUserSettings } from '../user/use-get-user-settings';
import { useGetAgentsList } from './use-get-agents-list';

export const useGetSelectedAgent = () => {
  const { mappedAgentsById, agentsList } = useGetAgentsList().data ?? {};
  const { data: userSettings } = useGetUserSettings();
  const { selectedAgent } = useAgentStore();

  const mostRecentAgentId = userSettings?.recent_agent_ids?.[0];
  const mostRecentAgent = mappedAgentsById && mostRecentAgentId ? mappedAgentsById[mostRecentAgentId] : null;

  return selectedAgent ?? mostRecentAgent ?? agentsList?.[0] ?? null;
};
