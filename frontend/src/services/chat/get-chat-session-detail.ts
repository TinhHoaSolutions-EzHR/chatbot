import { httpClient } from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { IChatSessionDetail } from '@/types/chat';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const getChatSessionDetail = async (chatSessionId: string): Promise<IChatSessionDetail> => {
  try {
    const res = await httpClient.get<IApiResponse<IChatSessionDetail>>(
      getApiUrl(ApiEndpointPrefix.CHAT, `/chat-sessions/${chatSessionId}`),
    );
    return res.data.data;
  } catch (error) {
    console.error('[GetChatSessionDetail]: ', error);
    throw error;
  }
};
