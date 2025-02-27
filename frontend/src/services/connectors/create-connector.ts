import { httpClient } from '@/lib/axios';
import { IApiResponse } from '@/types/api-response';
import { IConnector, IConnectorRequest } from '@/types/connector';
import { ApiEndpointPrefix, getApiUrl } from '@/utils/get-api-url';

export const createConnector = async (data: IConnectorRequest): Promise<IConnector> => {
  try {
    const res = await httpClient.post<IApiResponse<IConnector>>(getApiUrl(ApiEndpointPrefix.CONNECTORS), data);
    return res.data.data;
  } catch (error) {
    console.error('[CreateConnector], ', error);
    throw error;
  }
};
