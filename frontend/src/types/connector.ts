import { ITimestampResponse } from './common';

export enum DocumentSource {
  FILE = 'file',
  GOOGLE_DRIVE = 'google_drive',
}

export interface IConnector extends ITimestampResponse {
  id: string;
  name: string;
  source: DocumentSource;
  connector_specific_config?: {
    file_paths: string[];
  } | null;
}

export interface IConnectorRequest {
  name: string;
  file_paths: string[];
}
