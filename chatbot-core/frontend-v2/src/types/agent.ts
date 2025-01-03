import { IPrompt } from './prompt';

export enum AgentType {
  SYSTEM = 'system',
  USER = 'user',
}

export interface IAgent {
  id: string;
  name: string;
  description: string;
  agent_type: AgentType;
  is_visible: boolean;
  uploaded_image_path: string;
  created_at: string;
  updated_at: string;
  deleted_at: string;
}

export interface IAgentWithPrompts extends IAgent {
  prompts: IPrompt[];
}
