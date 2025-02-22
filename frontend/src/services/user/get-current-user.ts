import { httpClient } from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { IUser } from '@/types/user';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const getCurrentUser = async (): Promise<IUser> => {
  try {
    const res = await httpClient.get<IApiResponse<IUser>>(getApiUrl(ApiEndpointPrefix.USER));
    return res.data.data;
  } catch (error) {
    console.error('[GetUser]: ', error);
    throw error;
  }
};
