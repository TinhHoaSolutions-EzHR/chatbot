import { httpClient } from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { IFolder } from '@/types/chat';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

interface IEditChatFolderProps {
  folderId: string;
  folderName: string;
}

export const editChatFolder = async ({ folderId, folderName }: IEditChatFolderProps): Promise<IFolder> => {
  try {
    const res = await httpClient.patch<IApiResponse<IFolder>>(getApiUrl(ApiEndpointPrefix.FOLDER, `/${folderId}`), {
      name: folderName,
    });

    return res.data.data;
  } catch (error) {
    console.error('[EditChatFolder]: ', error);
    throw error;
  }
};
