import { ValidSources } from "../types";

export interface CredentialBase<T> {
  credential_json: T;
  admin_public: boolean;
  source: ValidSources;
  name?: string;
  curator_public?: boolean;
  groups?: number[];
}

export interface Credential<T> extends CredentialBase<T> {
  id: number;
  user_id: string | null;
  time_created: string;
  time_updated: string;
}

export interface ConfluenceCredentialJson {
  confluence_username: string;
  confluence_access_token: string;
}
export const credentialTemplates: Record<ValidSources, any> = {
  file: null,
};

