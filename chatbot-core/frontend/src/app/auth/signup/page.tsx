import { HealthCheckBanner } from "@/components/health/healthcheck";
import { User } from "@/lib/types";
import {
  getCurrentUserSS,
  getAuthTypeMetadataSS,
  AuthTypeMetadata,
  getAuthUrlSS,
} from "@/lib/userSS";
import { redirect } from "next/navigation";
import { EmailPasswordForm } from "../login/EmailPasswordForm";
import Text from "@/components/ui/text";
import Link from "next/link";
import AuthFlowContainer from "@/components/auth/AuthFlowContainer";

const Page = async (props: {
  searchParams?: Promise<{ [key: string]: string | string[] | undefined }>;
}) => {
  const searchParams = await props.searchParams;
  const nextUrl = Array.isArray(searchParams?.next)
    ? searchParams?.next[0]
    : searchParams?.next || null;

  // catch cases where the backend is completely unreachable here
  // without try / catch, will just raise an exception and the page
  // will not render
  let authTypeMetadata: AuthTypeMetadata | null = null;
  let currentUser: User | null = null;
  try {
    [authTypeMetadata, currentUser] = await Promise.all([
      getAuthTypeMetadataSS(),
      getCurrentUserSS(),
    ]);
  } catch (e) {
    console.log(`Some fetch failed for the login page - ${e}`);
  }

  // simply take the user to the home page if Auth is disabled
  if (authTypeMetadata?.authType === "disabled") {
    return redirect("/");
  }

  // if user is already logged in, take them to the main app page
  if (currentUser && currentUser.is_active) {
    if (!authTypeMetadata?.requiresVerification || currentUser.is_verified) {
      return redirect("/");
    }
    return redirect("/auth/waiting-on-verification");
  }

  // only enable this page if basic login is enabled
  if (authTypeMetadata?.authType !== "basic") {
    return redirect("/");
  }

  return (
    <AuthFlowContainer>
      <HealthCheckBanner />

      <>
        <div className="absolute top-10x w-full"></div>
        <div className="flex w-full flex-col justify-center">
          <h2 className="text-center text-xl text-strong font-bold">
            Sign Up for EzHR
          </h2>

          <EmailPasswordForm
            isSignup
            shouldVerify={authTypeMetadata?.requiresVerification}
            nextUrl={nextUrl}
          />

          <div className="flex">
            <Text className="mt-4 mx-auto">
              Already have an account?{" "}
              <Link
                href={{
                  pathname: "/auth/login",
                  query: { ...searchParams },
                }}
                className="text-link font-medium"
              >
                Log In
              </Link>
            </Text>
          </div>
        </div>
      </>
    </AuthFlowContainer>
  );
};

export default Page;
