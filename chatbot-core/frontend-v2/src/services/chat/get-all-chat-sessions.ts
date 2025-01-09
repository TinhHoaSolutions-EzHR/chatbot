import httpClient from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { IChatSession } from '@/types/chat';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const getAllChatSessions = async (): Promise<IChatSession[]> => {
  try {
    const res = await httpClient.get<IApiResponse<IChatSession[]>>(getApiUrl(ApiEndpointPrefix.CHAT, '/chat-sessions'));
    return res.data.data;
  } catch (error) {
    console.error('[GetAllChatSessions]: ', error);
    throw new Error("Error getting user's chat sessions");
  }
};
