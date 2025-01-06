import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

import AuthProvider from '@/providers/auth-provider/auth-provider';
import HealthCheckProvider from '@/providers/health-check-provider';
import TanstackQueryProvider from '@/providers/query-provider';

import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'EzHR Chatbot',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={inter.className}>
      <body className="antialiased">
        <TanstackQueryProvider>
          <HealthCheckProvider>
            <AuthProvider>{children}</AuthProvider>
          </HealthCheckProvider>
        </TanstackQueryProvider>
      </body>
    </html>
  );
}
