export enum ProviderType {
  OPENAI = 'openai',
  GEMINI = 'gemini',
  COHERE = 'cohere',
}

export interface IProvider {
  id: string;
  name: string;
  created_at: string;
  updated_at: string;
  deleted_at: string;
}
