import axios from 'axios';

import { getAuthUrl } from '@/utils/get-api-url';

export const getUserOauthAccessToken = async (code: string) => {
  try {
    await axios.get(getAuthUrl(`/oauth/google?code=${code}`));
    return true;
  } catch (error) {
    console.error('[UserAccessToken]: ', error);
    return false;
  }
};
