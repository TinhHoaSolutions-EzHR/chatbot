import { streamClient } from '@/lib/axios';
import { IChatMessageRequest } from '@/types/chat';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

interface ICreateChatMessageProps {
  chatSessionId: string;
  data: Partial<IChatMessageRequest>;
}

export const createChatMessage = async ({ chatSessionId, data }: ICreateChatMessageProps) => {
  try {
    const res = await streamClient.post(
      getApiUrl(ApiEndpointPrefix.CHAT, `/chat-sessions/${chatSessionId}/messages`),
      data,
    );

    const stream = res.data;

    for await (const chunk of stream) {
      console.error(chunk);
    }
  } catch (error) {
    console.error('[CreateChatMessage]: ', error);
    throw new Error('Error creating chat message');
  }
};
