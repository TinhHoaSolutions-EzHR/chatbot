import { ITimestampResponse } from './common';

export interface IPrompt extends ITimestampResponse {
  id: string;
  name: string;
  prompt: string;
}
