import httpClient from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { IFolder } from '@/types/chat';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const editChatFolder = async (folderId: string, folderName: string): Promise<IFolder> => {
  try {
    const res = await httpClient.patch<IApiResponse<IFolder>>(getApiUrl(ApiEndpointPrefix.FOLDER, `/${folderId}`), {
      name: folderName,
    });

    return res.data.data;
  } catch (error) {
    console.error('[EditChatFolder]: ', error);
    throw new Error('Error editing chat folder');
  }
};
