import { httpClient } from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { IChatSession } from '@/types/chat';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const createChatSession = async (agentId: string): Promise<IChatSession> => {
  try {
    const res = await httpClient.post<IApiResponse<IChatSession>>(getApiUrl(ApiEndpointPrefix.CHAT, '/chat-sessions'), {
      agent_id: agentId,
    });
    return res.data.data;
  } catch (error) {
    console.error('[CreateChatSession]: ', error);
    throw new Error('Error creating chat session');
  }
};
