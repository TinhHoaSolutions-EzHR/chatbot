export enum AgentType {
  SYSTEM = 'system',
  USER = 'user',
}

export interface IAgent {
  id: string;
  user_id: string;
  name: string;
  prompt: string;
  description?: string;
  agent_type: AgentType;
  is_visible: boolean;
  uploaded_image_path: string | null;
  created_at: string;
  updated_at: string;
  deleted_at: string | null;
}

export interface IAgentWithStarterMessages extends IAgent {
  starter_messages: string[];
}
