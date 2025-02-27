import { httpClient } from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { IIndexStatusResponse } from '@/types/document';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const getIndexStatus = async (taskId: string): Promise<IIndexStatusResponse> => {
  try {
    const res = await httpClient.get<IApiResponse<IIndexStatusResponse>>(
      getApiUrl(ApiEndpointPrefix.BACKGROUND_TASKS, `/${taskId}/status`),
    );
    return res.data.data;
  } catch (error) {
    console.error('[GetIndexStatus]: ', error);
    throw error;
  }
};
