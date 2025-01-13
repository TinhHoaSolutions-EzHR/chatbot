export enum DocumentSource {
  FILE = 'file',
  GOOGLE_DRIVE = 'google_drive',
}

export interface IConnector {
  id: string;
  name: string;
  source: DocumentSource;
  connector_specific_config?: string | null;
  created_at: string;
  updated_at: string;
  deleted_at?: string | null;
}
