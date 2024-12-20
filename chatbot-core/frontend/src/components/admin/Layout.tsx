import { User, UserRole } from '@/lib/types';
import { AuthTypeMetadata, getAuthTypeMetadataSS, getCurrentUserSS } from '@/lib/userSS';
import { redirect } from 'next/navigation';
import { ClientLayout } from './ClientLayout';
import { AnnouncementBanner } from '../header/AnnouncementBanner';
import React from 'react';

export async function Layout({ children }: { children: React.ReactNode }) {
  const tasks = [await getAuthTypeMetadataSS(), await getCurrentUserSS()];

  // catch cases where the backend is completely unreachable here
  // without try / catch, will just raise an exception and the page
  // will not render
  let results: (User | AuthTypeMetadata | null)[] = [null, null];
  try {
    results = await Promise.all(tasks);
  } catch (e) {
    console.log(`Some fetch failed for the main search page - ${e}`);
  }

  const authTypeMetadata = results[0] as AuthTypeMetadata | null;
  const user = results[1] as User | null;
  const authDisabled = authTypeMetadata?.authType === 'disabled';
  const requiresVerification = authTypeMetadata?.requiresVerification;

  if (!authDisabled) {
    if (!user) {
      return redirect('/auth/login');
    }
    if (user.role === UserRole.BASIC) {
      return redirect('/');
    }
    if (!user.is_verified && requiresVerification) {
      return redirect('/auth/waiting-on-verification');
    }
  }

  return (
    <ClientLayout user={user}>
      <AnnouncementBanner />
      {children}
    </ClientLayout>
  );
}
