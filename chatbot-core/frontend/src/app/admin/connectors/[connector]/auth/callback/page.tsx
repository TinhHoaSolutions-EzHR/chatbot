"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function CallbackPage() {
  const router = useRouter();

  useEffect(() => {
    const connector = window.location.pathname.split("/")[3]; // Extract connector from path
    const authCookieName = connector === "gmail"
      ? "GMAIL_AUTH_IS_ADMIN_COOKIE_NAME"
      : "GOOGLE_DRIVE_AUTH_IS_ADMIN_COOKIE_NAME";

    // Check if the user has the necessary authentication cookie
    const authCookie = document.cookie
      .split("; ")
      .find(row => row.startsWith(authCookieName));

    if (authCookie?.includes("true")) {
      // Redirect to the admin connector page
      router.push(`/admin/connectors/${connector}`);
    } else {
      // Redirect to user connectors page
      router.push("/user/connectors");
    }
  }, [router]);

  return <div>Loading...</div>;
}
export const dynamic = "force-static";
export const revalidate = 3600;