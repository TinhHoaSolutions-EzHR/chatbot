interface UserPreferences {
  chosen_assistants: number[] | null;
  visible_assistants: number[];
  hidden_assistants: number[];
  default_model: string | null;
}

export enum UserStatus {
  live = 'live',
  invited = 'invited',
  deactivated = 'deactivated',
}

export enum UserRole {
  BASIC = 'basic',
  ADMIN = 'admin',
  CURATOR = 'curator',
  GLOBAL_CURATOR = 'global_curator',
}

export const USER_ROLE_LABELS: Record<UserRole, string> = {
  [UserRole.BASIC]: 'Basic',
  [UserRole.ADMIN]: 'Admin',
  [UserRole.GLOBAL_CURATOR]: 'Global Curator',
  [UserRole.CURATOR]: 'Curator',
};

export interface User {
  id: string;
  email: string;
  is_active: string;
  is_superuser: string;
  is_verified: string;
  role: UserRole;
  preferences: UserPreferences;
  status: UserStatus;
  current_token_created_at?: Date;
  current_token_expiry_length?: number;
  oidc_expiry?: Date;
  is_cloud_superuser?: boolean;
  organization_name: string | null;
}
