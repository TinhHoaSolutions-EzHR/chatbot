"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export const dynamic = "force-static"; // Ensure this page is statically exported

export default function SAMLCallbackPage() {
  const router = useRouter();

  useEffect(() => {
    // Get query parameters from the URL (to simulate request query and form data)
    const searchParams = new URLSearchParams(window.location.search);

    // Simulate form submission to backend
    const formData = new FormData();
    searchParams.forEach((value, key) => {
      formData.append(key, value);
    });

    // Simulate sending the form data via POST (for example, using fetch)
    fetch("/auth/saml/callback", {
      method: "POST",
      body: formData,
      headers: {
        "X-Forwarded-Host": window.location.host,
        "X-Forwarded-Port": window.location.port,
      },
    })
      .then((response) => {
        if (!response.ok) {
          // If the response is not OK, redirect to the error page
          router.push("/auth/error");
        } else {
          // If response is OK, check for the set-cookie header
          const setCookieHeader = response.headers.get("set-cookie");

          if (!setCookieHeader) {
            // If no cookie header, redirect to the error page
            router.push("/auth/error");
          } else {
            // Otherwise, set the cookie and redirect to the homepage or appropriate URL
            const redirectUrl = "/"; // You can set this dynamically based on your logic
            const redirectResponse = new Response("", {
              status: 303, // See other (redirect status)
              headers: {
                Location: redirectUrl,
                "Set-Cookie": setCookieHeader, // Set the cookie for the session
              },
            });

            // Perform the redirection
            router.push(redirectResponse.headers.get("Location") || "/");
          }
        }
      })
      .catch(() => {
        // Handle fetch errors and redirect to the error page
        router.push("/auth/error");
      });
  }, [router]);

  return <div>Loading...</div>; // Show loading while processing the request
}
