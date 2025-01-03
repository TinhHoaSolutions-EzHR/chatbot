import { MOCK_AGENTS_LIST } from '@/configs/mock-agents';
import { IAgent } from '@/types/agent';

export const getAgentsList: () => Promise<IAgent[]> = async () => {
  return new Promise<IAgent[]>(resolve => {
    resolve(MOCK_AGENTS_LIST);
  });
};
