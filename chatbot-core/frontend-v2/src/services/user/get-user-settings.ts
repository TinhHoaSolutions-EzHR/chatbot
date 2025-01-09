import httpClient from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { IUserSettings } from '@/types/user';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const getUserSettings = async (): Promise<IUserSettings> => {
  try {
    const res = await httpClient.get<IApiResponse<IUserSettings>>(getApiUrl(ApiEndpointPrefix.USER, '/settings'));
    return res.data.data;
  } catch (error) {
    console.error('[GetUserSettings]: ', error);
    throw new Error('Error getting user settings');
  }
};
