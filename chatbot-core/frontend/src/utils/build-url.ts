import { ApiEndpoint } from '@/constants/api';
import { INTERNAL_URL } from '@/constants/env';

export const getApiUrl = (endpoint: ApiEndpoint, searchParams?: string): string => {
  return `${INTERNAL_URL}${endpoint}${searchParams ? `?${searchParams}` : ''}`;
};
