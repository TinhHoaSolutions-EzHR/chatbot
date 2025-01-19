import { httpClient } from '@/lib/axios';
import { IAgent } from '@/types/agent';
import { IApiResponse } from '@/types/api-response';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const getAgentsList: () => Promise<IAgent[]> = async () => {
  try {
    const res = await httpClient.get<IApiResponse<IAgent[]>>(getApiUrl(ApiEndpointPrefix.AGENTS));
    return res.data.data;
  } catch (error) {
    console.error('[GetAgentsList]: ', error);
    throw error;
  }
};
