import { httpClient } from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { IFolder } from '@/types/chat';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const createChatFolder = async (folderName: string): Promise<IFolder> => {
  try {
    const res = await httpClient.post<IApiResponse<IFolder>>(getApiUrl(ApiEndpointPrefix.FOLDER), {
      name: folderName,
    });
    return res.data.data;
  } catch (error) {
    console.error('[CreateChatFolder]: ', error);
    throw new Error('Error creating chat folder');
  }
};
