import { ITimestampResponse } from './common';

export enum UserRole {
  ADMIN = 'admin',
  BASIC = 'basic',
}

export interface IUser extends ITimestampResponse {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: UserRole;
}

export interface IUserSettings {
  recent_agent_ids?: string[];
  auto_scroll: boolean;
}
