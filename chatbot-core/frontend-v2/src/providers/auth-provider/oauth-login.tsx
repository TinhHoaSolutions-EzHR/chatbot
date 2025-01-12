'use client';

import { Loader2 } from 'lucide-react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

import AppLogo from '@/components/app-logo';
import GoogleIcon from '@/components/google-icon';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
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
    <div className="full-screen-center bg-muted">
      <Card className="w-full max-w-96 mx-4">
        <CardHeader className="pb-4">
          <CardTitle className="w-full flex justify-center">
            <AppLogo className="w-44" />
          </CardTitle>
          <CardDescription className="text-center pt-2">
            App chatbot for easier management over your own information.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Separator className="pt-[2px]" />
          <Link href={GOOGLE_OAUTH_URL}>
            <Button variant="outline" className="w-full mt-4" size="lg">
              <GoogleIcon size={24} />
              Sign in with google
            </Button>
          </Link>
          <p className="text-sm text-muted-foreground text-center mt-2">
            Cannot sign in?{' '}
            <Link
              href="/supports"
              className="underline underline-offset-3 text-zinc-600 font-medium hover:text-zinc-800"
            >
              Get supports.
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  );
};
