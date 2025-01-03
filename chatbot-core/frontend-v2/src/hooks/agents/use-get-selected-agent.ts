import { useAgentStore } from '../stores/use-agent-store';
import { useGetRecentAgents } from './use-get-recent-agents';

export const useGetSelectedAgent = () => {
  const { data: recentAgents } = useGetRecentAgents();
  const { selectedAgent } = useAgentStore();

  return selectedAgent ?? recentAgents?.[0] ?? null;
};
