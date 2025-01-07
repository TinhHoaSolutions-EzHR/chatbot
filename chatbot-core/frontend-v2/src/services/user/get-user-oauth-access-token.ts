import api from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { getAuthUrl } from '@/utils/get-api-url';

interface IAccessToken {
  access_token: string;
  token_type: string;
}

export const getUserOauthAccessToken = async (code: string): Promise<IAccessToken> => {
  try {
    const res = await api.get<IApiResponse<IAccessToken>>(getAuthUrl(`/oauth/google?code=${code}`));
    return res.data.data;
  } catch (error) {
    // We want to show the Error here, however, we still throw the Error
    // once again for the `useQuery` to catch it.
    console.error('[UserAccessToken]: ', error);
    throw new Error('Error getting user access token');
  }
};
