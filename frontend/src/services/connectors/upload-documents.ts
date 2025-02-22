import { httpClient } from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const uploadDocuments = async (documents: File[]): Promise<string[]> => {
  try {
    const formData = new FormData();

    for (const document of documents) {
      formData.append('documents', document);
    }

    const res = await httpClient.post<IApiResponse<string[]>>(
      getApiUrl(ApiEndpointPrefix.CONNECTORS, '/documents/upload'),
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      },
    );

    return res.data.data;
  } catch (error) {
    console.error('[UploadDocuments]: ', error);
    throw error;
  }
};
