export enum UserRole {
  ADMIN = 'admin',
  BASIC = 'basic',
}

export interface IUser {
  id: string;
  email: string;
  avatar?: string;
  role: UserRole;
  created_at: string;
  updated_at: string;
}

export interface IUserSettings {
  recent_agent_ids?: string[];
  auto_scroll: boolean;
}
