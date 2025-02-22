import { httpClient } from '@/lib/axios';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const deleteChatFolder = async (folderId: string) => {
  try {
    await httpClient.delete(getApiUrl(ApiEndpointPrefix.FOLDER, `/${folderId}`));
  } catch (error) {
    console.error('[DeleteChatFolder]: ', error);
    throw error;
  }
};
