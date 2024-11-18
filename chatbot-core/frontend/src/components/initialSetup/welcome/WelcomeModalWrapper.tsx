import {
  _CompletedWelcomeFlowDummyComponent,
  _WelcomeModal,
} from "./WelcomeModal";
import { COMPLETED_WELCOME_FLOW_COOKIE } from "./constants";
import { User } from "@/lib/types";

export function hasCompletedWelcomeFlowSS(requestCookies: {
  [key: string]: string;
}) {
  return (
    requestCookies[COMPLETED_WELCOME_FLOW_COOKIE]?.toLowerCase() === "true"
  );
}

export function WelcomeModal({
  user,
  requestCookies,
}: {
  user: User | null;
  requestCookies: { [key: string]: string };
}) {
  const hasCompletedWelcomeFlow = hasCompletedWelcomeFlowSS(requestCookies);
  if (hasCompletedWelcomeFlow) {
    return <_CompletedWelcomeFlowDummyComponent />;
  }

  return <_WelcomeModal user={user} />;
}
