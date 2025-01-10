import { httpClient } from '@/lib/axios';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const deleteChatSession = async (chatSessionId: string): Promise<void> => {
  try {
    await httpClient.delete(getApiUrl(ApiEndpointPrefix.CHAT, `/chat-sessions/${chatSessionId}`));
  } catch (error) {
    console.error('[DeleteChatSession]: ', error);
    throw new Error('Error deleting chat session');
  }
};
