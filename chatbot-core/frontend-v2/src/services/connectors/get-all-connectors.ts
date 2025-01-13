import { httpClient } from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { IConnector } from '@/types/connector';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const getAllConnectors = async (): Promise<IConnector[]> => {
  try {
    const res = await httpClient.get<IApiResponse<IConnector[]>>(getApiUrl(ApiEndpointPrefix.CONNECTORS));
    return res.data.data;
  } catch (error) {
    console.error('[GetAllConnectors]: ', error);
    throw new Error('Error getting all connectors');
  }
};
