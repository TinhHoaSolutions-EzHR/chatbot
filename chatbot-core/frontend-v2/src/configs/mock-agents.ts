import { AgentType, IAgent } from '@/types/agent';

export const MOCK_AGENTS_LIST: IAgent[] = [
  {
    id: '1',
    agent_type: AgentType.SYSTEM,
    name: 'System Agent',
    description: 'System Agent Description',
    is_visible: true,
    uploaded_image_path: '',
    created_at: '',
    updated_at: '',
    deleted_at: '',
  },
  {
    id: '2',
    agent_type: AgentType.SYSTEM,
    name: 'System Agent 2',
    description: 'System Agent 2 Description',
    is_visible: true,
    uploaded_image_path: '',
    created_at: '',
    updated_at: '',
    deleted_at: '',
  },
  {
    id: '3',
    agent_type: AgentType.USER,
    name: 'User Agent',
    description: 'User Agent Description',
    is_visible: true,
    uploaded_image_path: '',
    created_at: '',
    updated_at: '',
    deleted_at: '',
  },
];

export const MOCK_RECENT_AGENTS: IAgent[] = [MOCK_AGENTS_LIST[2], MOCK_AGENTS_LIST[0]];
