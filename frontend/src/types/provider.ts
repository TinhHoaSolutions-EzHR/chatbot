import { ITimestampResponse } from './common';

export enum ProviderType {
  OPENAI = 'openai',
  GEMINI = 'gemini',
  COHERE = 'cohere',
}

export interface IProvider extends ITimestampResponse {
  id: string;
  name: string;
}
