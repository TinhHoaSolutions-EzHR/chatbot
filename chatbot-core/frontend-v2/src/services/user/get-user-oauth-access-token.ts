import { httpClient } from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { AuthEndpoint } from '@/utils/get-api-url';

interface IAccessToken {
  access_token: string;
  token_type: string;
}

export const getUserOauthAccessToken = async (code: string): Promise<IAccessToken> => {
  try {
    const res = await httpClient.get<IApiResponse<IAccessToken>>(AuthEndpoint.GOOGLE_OAUTH, {
      params: {
        code,
      },
    });
    return res.data.data;
  } catch (error) {
    console.error('[UserAccessToken]: ', error);
    throw error;
  }
};
