import { cookies } from "next/headers";
import { User } from "./types";
import { buildUrl } from "./utilsSS";
import { ReadonlyRequestCookies } from "next/dist/server/web/spec-extension/adapters/request-cookies";
import { AuthType } from "./constants";

export interface AuthTypeMetadata {
  authType: AuthType;
  autoRedirect: boolean;
  requiresVerification: boolean;
}

export const getAuthTypeMetadataSS = async (): Promise<AuthTypeMetadata> => {
  const res = await fetch(buildUrl("/auth/type"));
  if (!res.ok) {
    throw new Error("Failed to fetch data");
  }

  const data: { auth_type: string; requires_verification: boolean } =
    await res.json();

  let authType: AuthType;

  authType = data.auth_type as AuthType;

  return {
    authType,
    autoRedirect: false,
    requiresVerification: data.requires_verification,
  };
};

export const getAuthDisabledSS = async (): Promise<boolean> => {
  return (await getAuthTypeMetadataSS()).authType === "disabled";
};

export const getAuthUrlSS = async (
  authType: AuthType,
  nextUrl: string | null
): Promise<string> => {
  // Returns the auth url for the given auth type
  switch (authType) {
    case "disabled":
      return "";
    case "basic":
      return "";
  }
};

const logoutStandardSS = async (headers: Headers): Promise<Response> => {
  return await fetch(buildUrl("/auth/logout"), {
    method: "POST",
    headers: headers,
  });
};

export const logoutSS = async (
  authType: AuthType,
  headers: Headers
): Promise<Response | null> => {
  switch (authType) {
    case "disabled":
      return null;
    default: {
      return await logoutStandardSS(headers);
    }
  }
};

export const getCurrentUserSS = async (): Promise<User | null> => {
  try {
    const response = await fetch(buildUrl("/me"), {
      credentials: "include",
      next: { revalidate: 0 },
      headers: {
        cookie: (
          await cookies()
        )
          .getAll()
          .map((cookie) => `${cookie.name}=${cookie.value}`)
          .join("; "),
      },
    });
    if (!response.ok) {
      return null;
    }
    const user = await response.json();
    return user;
  } catch (e) {
    console.log(`Error fetching user: ${e}`);
    return null;
  }
};

export const processCookies = (cookies: ReadonlyRequestCookies): string => {
  return cookies
    .getAll()
    .map((cookie) => `${cookie.name}=${cookie.value}`)
    .join("; ");
};
