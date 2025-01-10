import { httpClient } from '@/lib/axios';
import { IAgentWithStarterMessages } from '@/types/agent';
import { IApiResponse } from '@/types/api-response';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const getAgentDetail: (agentId: string) => Promise<IAgentWithStarterMessages> = async agentId => {
  try {
    const res = await httpClient.get<IApiResponse<IAgentWithStarterMessages>>(
      getApiUrl(ApiEndpointPrefix.AGENTS, `/${agentId}`),
    );
    return res.data.data;
  } catch (error) {
    console.error('[GetAgentDetail]: ', error);
    throw new Error('Error getting agent detail');
  }
};
