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
