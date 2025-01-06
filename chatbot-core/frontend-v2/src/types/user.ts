export enum UserRole {
  ADMIN = 'ADMIN',
  BASIC = 'BASIC',
}

export interface IUser {
  id: string;
  email: string;
  avatar?: string;
  role: UserRole;
  created_at: string;
  updated_at: string;
}
