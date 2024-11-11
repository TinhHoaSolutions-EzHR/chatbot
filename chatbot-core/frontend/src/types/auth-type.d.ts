export type AuthType = 'disabled' | 'basic' | 'google_oauth' | 'oidc' | 'saml' | 'cloud';

export interface AuthTypeMetadata {
  authType: AuthType;
  autoRedirect: boolean;
  requiresVerification: boolean;
}
