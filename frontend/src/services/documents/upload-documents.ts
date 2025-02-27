import { httpClient } from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { IDocumentUploadResponse } from '@/types/document';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const uploadDocuments = async (documents: File[]): Promise<IDocumentUploadResponse[]> => {
  try {
    const formData = new FormData();

    for (const document of documents) {
      formData.append('uploaded_documents', document);
    }

    const res = await httpClient.post<IApiResponse<IDocumentUploadResponse[]>>(
      getApiUrl(ApiEndpointPrefix.DOCUMENTS, '/upload'),
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
