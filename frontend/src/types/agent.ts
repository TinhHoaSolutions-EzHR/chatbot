import { ITimestampResponse } from './common';

export enum AgentType {
  SYSTEM = 'system',
  USER = 'user',
}

export interface IAgent extends ITimestampResponse {
  id: string;
  user_id: string;
  name: string;
  prompt: string;
  description?: string;
  agent_type: AgentType;
  is_visible: boolean;
  uploaded_image_path: string | null;
}

export interface IStarterMessage extends ITimestampResponse {
  id: string;
  agent_id: string;
  name: string;
  message: string;
}

export interface IAgentWithStarterMessages extends IAgent {
  starter_messages: IStarterMessage[];
}
