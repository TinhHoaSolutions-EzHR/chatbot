import { streamClient } from '@/lib/axios';
import { IChatMessageRequest } from '@/types/chat';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

interface ICreateChatMessageProps {
  chatSessionId: string;
  data: Partial<IChatMessageRequest>;
  abortController: AbortController;
}

export const createChatMessage = async ({
  chatSessionId,
  data,
  abortController,
}: ICreateChatMessageProps): Promise<ReadableStream> => {
  try {
    const res = await streamClient.post<ReadableStream>(
      getApiUrl(ApiEndpointPrefix.CHAT, `/chat-sessions/${chatSessionId}/messages`),
      data,
      {
        signal: abortController.signal,
      },
    );

    return res.data;
  } catch (error) {
    console.error('[CreateChatMessage]: ', error);
    throw error;
  }
};
