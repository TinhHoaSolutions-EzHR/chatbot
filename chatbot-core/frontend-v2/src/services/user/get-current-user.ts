import axios from 'axios';

import { IUser } from '@/types/user';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const getCurrentUser = async (): Promise<IUser | null> => {
  try {
    const res = await axios.get<IUser>(getApiUrl(ApiEndpointPrefix.USER));
    return res.data;
  } catch (error) {
    console.error('[GetUser]: ', error);
    return null;
  }
};
