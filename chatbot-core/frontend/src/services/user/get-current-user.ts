import { ApiEndpoint } from '@/constants/api';
import { User } from '@/types/user';
import { getApiUrl } from '@/utils/build-url';
import axios from 'axios';

export const getCurrentUser = async (): Promise<User | null> => {
  try {
    const response = await axios.get(getApiUrl(ApiEndpoint.ME), {
      withCredentials: true,
    });

    const user = response.data;
    return user;
  } catch (error) {
    console.error(error);
    return null;
  }
};
