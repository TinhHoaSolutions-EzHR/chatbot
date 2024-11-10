"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export const dynamic = "force-static"; // Ensure this is statically exported

export default function OIDCCallbackPage() {
  const router = useRouter();

  useEffect(() => {
    const searchParams = new URLSearchParams(window.location.search);
    const connector = searchParams.get("connector");

    // Simulate the fetch for the callback (like checking cookies)
    const authCookieName = connector === "gmail"
      ? "GMAIL_AUTH_IS_ADMIN_COOKIE_NAME"
      : "GOOGLE_DRIVE_AUTH_IS_ADMIN_COOKIE_NAME";

    // Check for the cookie on the client side
    const authStatus = document.cookie.includes(authCookieName);

    if (!authStatus) {
      router.push("/auth/create-account"); // Redirect to account creation if not authenticated
      return;
    }

    // If authenticated, proceed to the redirect URL (you can simulate fetching the location header)
    const redirectUrl = searchParams.get("redirect_url") || "/"; // Or default to home
    router.push(redirectUrl); // Redirect to the URL
  }, [router]);

  return <div>Loading...</div>; // Show a loading state while checking auth status
}
