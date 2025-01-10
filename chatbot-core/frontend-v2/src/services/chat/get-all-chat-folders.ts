import { httpClient } from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { IFolder } from '@/types/chat';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const getAllChatFolders = async (): Promise<IFolder[]> => {
  try {
    const res = await httpClient.get<IApiResponse<IFolder[]>>(getApiUrl(ApiEndpointPrefix.FOLDER));
    return res.data.data;
  } catch (error) {
    console.error('[GetAllChatFolders]: ', error);
    throw new Error('Error getting all chat folders');
  }
};
