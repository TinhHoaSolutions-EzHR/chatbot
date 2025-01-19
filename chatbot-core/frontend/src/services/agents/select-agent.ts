import { httpClient } from '@/lib/axios';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const selectAgent = async (agentId: string): Promise<void> => {
  try {
    await httpClient.patch(getApiUrl(ApiEndpointPrefix.USER, '/settings'), {
      current_agent_id: agentId,
    });
  } catch (error) {
    console.error('[SelectAgent]: ', error);
    throw error;
  }
};
