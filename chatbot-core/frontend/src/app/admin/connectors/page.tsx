import { ConfigurableSources } from "@/lib/types";
import ConnectorWrapper from "./ConnectorWrapper";

export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ c: string }>;
}) {
  const params = await searchParams;
  const c = params.c;

  return (
    <ConnectorWrapper connector={c.replace("-", "_") as ConfigurableSources} />
  );
}
