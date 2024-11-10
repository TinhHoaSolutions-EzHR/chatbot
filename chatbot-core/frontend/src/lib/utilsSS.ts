"use client";
import { HOST_URL, INTERNAL_URL } from "./constants";
import Cookies from "js-cookie";
import type { RequestInit } from "next/dist/server/web/spec-extension/request";

// Helper function to build full URL for client requests
export function buildClientUrl(path: string) {
  return path.startsWith("/") ? `${HOST_URL}${path}` : `${HOST_URL}/${path}`;
}

// Helper function to build full URL for internal requests
export function buildUrl(path: string) {
  return path.startsWith("/")
    ? `${INTERNAL_URL}${path}`
    : `${INTERNAL_URL}/${path}`;
}

// Function to fetch data with cookies included
export async function fetchSS(url: string, options?: RequestInit) {
  let cookieHeader = "";

  cookieHeader = Object.entries(Cookies.get() || {})
    .map(([name, value]) => `${name}=${value}`)
    .join("; ");

  // Ensure headers are correctly set
  const headers: HeadersInit = {
    ...(options?.headers || {}),
    cookie: cookieHeader, // Attach the cookie header
  };

  const init: RequestInit = {
    ...options,
    credentials: "include", // Include credentials (cookies) in requests
    cache: "no-store", // Disable caching
    headers, // Pass the updated headers with cookies
  };

  // Perform the fetch request with the constructed URL and options
  return fetch(buildUrl(url), init);
}
