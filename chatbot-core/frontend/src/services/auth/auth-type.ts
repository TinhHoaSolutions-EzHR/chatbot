import { ApiEndpoint } from '@/constants/api';
import { SERVER_SIDE_ONLY__CLOUD_ENABLED } from '@/constants/env';
import { AuthType, AuthTypeMetadata } from '@/types/auth-type';
import { getApiUrl } from '@/utils/build-url';
import axios from 'axios';

export const getAuthTypeMetadata = async (): Promise<AuthTypeMetadata> => {
  try {
    const response = await axios.get(getApiUrl(ApiEndpoint.AUTH_TYPE));

    const data: { auth_type: string; requires_verification: boolean } = response.data;

    const authType = SERVER_SIDE_ONLY__CLOUD_ENABLED ? 'cloud' : (data.auth_type as AuthType);

    // For SAML / OIDC, we auto-redirect the user to the IdP when the user visits
    // EzHR in an un-authenticated state
    if (authType === 'oidc' || authType === 'saml') {
      return {
        authType,
        autoRedirect: true,
        requiresVerification: data.requires_verification,
      };
    }

    return {
      authType,
      autoRedirect: false,
      requiresVerification: data.requires_verification,
    };
  } catch (error) {
    console.error('Failed to fetch data', error);
    throw new Error('Failed to fetch data');
  }
};
