import { ConfigurableSources } from "@/lib/types";
import ConnectorWrapper from "./ConnectorWrapper";

export default async function Page() {
  return (
    <ConnectorWrapper connector={"file" as ConfigurableSources} />
  );
}
