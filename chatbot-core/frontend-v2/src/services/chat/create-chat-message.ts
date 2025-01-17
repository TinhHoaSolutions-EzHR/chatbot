import { streamClient } from '@/lib/axios';
import { IChatMessageRequest } from '@/types/chat';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

interface ICreateChatMessageProps {
  chatSessionId: string;
  data: Partial<IChatMessageRequest>;
}

export const createChatMessage = async ({
  chatSessionId,
  data,
}: ICreateChatMessageProps): Promise<ReadableStream<any>> => {
  try {
    const res = await streamClient.post<ReadableStream>(
      getApiUrl(ApiEndpointPrefix.CHAT, `/chat-sessions/${chatSessionId}/messages`),
      data,
    );

    return res.data;
  } catch (error) {
    console.error('[CreateChatMessage]: ', error);
    throw error;
  }
};
