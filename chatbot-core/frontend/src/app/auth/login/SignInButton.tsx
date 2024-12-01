export function SignInButton({ authorizeUrl }: { authorizeUrl: string }) {
  const url = new URL(authorizeUrl);
  const finalAuthorizeUrl = url.toString();
  return (
    <a
      className="mx-auto mt-6 py-3 w-full text-text-100 bg-accent flex rounded cursor-pointer hover:bg-indigo-800"
      href={finalAuthorizeUrl}
    >
      Click here to sign in
    </a>
  );
}
