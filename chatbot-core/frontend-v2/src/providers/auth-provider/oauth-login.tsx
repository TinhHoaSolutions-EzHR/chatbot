import { Loader2 } from 'lucide-react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

import { Button } from '@/components/ui/button';
import { GOOGLE_OAUTH_URL } from '@/configs/google-oauth';
import { QueryParams } from '@/constants/misc';
import { useGetUserOauthAccessToken } from '@/hooks/user/use-get-user-oauth-access-token';

export const OauthLogin = () => {
  const [oauthCode, setOauthCode] = useState<string | undefined>();

  const searchParams = useSearchParams();
  const router = useRouter();

  const { isLoading } = useGetUserOauthAccessToken(oauthCode);

  useEffect(() => {
    const code = searchParams.get(QueryParams.OAUTH_CODE);

    if (!code) {
      return;
    }

    setOauthCode(code);
    router.replace('/');
  }, []);

  if (isLoading) {
    return (
      <div className="full-screen-center">
        <Loader2 size={32} className="animate-spin" />
      </div>
    );
  }

  return (
    <div className="full-screen-center">
      <Link href={GOOGLE_OAUTH_URL}>
        <Button>Sign in with Google</Button>
      </Link>
    </div>
  );
};
