export type AuthType =
  | "disabled"
  | "basic"
  | "google_oauth"
  | "oidc"
  | "saml"
  | "cloud";

export const HOST_URL = process.env.WEB_DOMAIN || "http://127.0.0.1:3000";
export const INTERNAL_URL = process.env.INTERNAL_URL || "http://127.0.0.1:5000";

export const NEXT_PUBLIC_NEW_CHAT_DIRECTS_TO_SAME_PERSONA =
  process.env.NEXT_PUBLIC_NEW_CHAT_DIRECTS_TO_SAME_PERSONA?.toLowerCase() ===
  "true";
export const GOOGLE_DRIVE_AUTH_IS_ADMIN_COOKIE_NAME =
  "google_drive_auth_is_admin";
export const AGENTIC_SEARCH_TYPE_COOKIE_NAME = "agentic_type";
export const LOGOUT_DISABLED =
  process.env.NEXT_PUBLIC_DISABLE_LOGOUT?.toLowerCase() === "true";
// Default sidebar open is true if the environment variable is not set
export const NEXT_PUBLIC_DEFAULT_SIDEBAR_OPEN =
  process.env.NEXT_PUBLIC_DEFAULT_SIDEBAR_OPEN?.toLowerCase() === "true" ??
  true;
export const TOGGLED_CONNECTORS_COOKIE_NAME = "toggled_connectors";
export const NEXT_PUBLIC_CUSTOM_REFRESH_URL =
  process.env.NEXT_PUBLIC_CUSTOM_REFRESH_URL;

export const DISABLE_LLM_DOC_RELEVANCE =
  process.env.DISABLE_LLM_DOC_RELEVANCE?.toLowerCase() === "true";

export const NEXT_PUBLIC_CLOUD_ENABLED =
  process.env.NEXT_PUBLIC_CLOUD_ENABLED?.toLowerCase() === "true";

export const REGISTRATION_URL =
  process.env.INTERNAL_URL || "http://127.0.0.1:3001";

export const SERVER_SIDE_ONLY__CLOUD_ENABLED =
  process.env.NEXT_PUBLIC_CLOUD_ENABLED?.toLowerCase() === "true";
