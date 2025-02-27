export interface IDocumentUploadResponse {
  task_id: string;
  document_url: string;
}

export enum IndexStatus {
  STARTED = 'STARTED',
  PENDING = 'PENDING',
  SUCCESS = 'SUCCESS',
  FAILURE = 'FAILURE',
}

export interface IIndexStatusResponse {
  task_id: string;
  status: IndexStatus;
}
