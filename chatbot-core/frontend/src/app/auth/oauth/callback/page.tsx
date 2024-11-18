// src/app/auth/oauth/callback/page.tsx

"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export const dynamic = "force-static"; // Make sure this is statically exported

export default function OAuthCallbackPage() {
  const router = useRouter();

  useEffect(() => {
    const searchParams = new URLSearchParams(window.location.search);
    const connector = searchParams.get("connector");
    const authCookieName = connector === "gmail"
      ? "GMAIL_AUTH_IS_ADMIN_COOKIE_NAME"
      : "GOOGLE_DRIVE_AUTH_IS_ADMIN_COOKIE_NAME";

    // Simulate the fetch for the callback (which in real cases would be an API request)
    const authStatus = document.cookie.includes(authCookieName); // Example of checking cookie

    if (!authStatus) {
      router.push("/auth/create-account"); // Redirect to account creation if not authenticated
      return;
    }

    // If we have the cookie, simulate getting a redirect URL (this would be dynamic in real cases)
    const redirectUrl = "/"; // Use the location header or default to "/"
    router.push(redirectUrl); // Redirect the user based on the status
  }, [router]);

  return <div>Loading...</div>;
}
