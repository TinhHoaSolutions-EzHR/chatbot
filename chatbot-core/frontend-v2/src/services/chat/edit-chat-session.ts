import { httpClient } from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { IChatSession, IChatSessionRequest } from '@/types/chat';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const editChatSession = async (
  chatSessionId: string,
  data: Partial<IChatSessionRequest>,
): Promise<IChatSession> => {
  try {
    const res = await httpClient.patch<IApiResponse<IChatSession>>(
      getApiUrl(ApiEndpointPrefix.CHAT, `/chat-sessions/${chatSessionId}`),
      data,
    );
    return res.data.data;
  } catch (error) {
    console.error('[EditChatSession]: ', error);
    throw new Error('Error editing chat session');
  }
};
