import { Connector } from "@/lib/connectors/connectors";
import { getSourceMetadata } from "@/lib/sources";

import Link from "next/link";

interface ConnectorTitleProps {
  connector: Connector<any>;
  ccPairId: number;
  ccPairName: string | null | undefined;
  isPublic?: boolean;
  owner?: string;
  isLink?: boolean;
  showMetadata?: boolean;
}

export const ConnectorTitle = ({
  connector,
  ccPairId,
  ccPairName,
  owner,
  isPublic = true,
  isLink = true,
  showMetadata = true,
}: ConnectorTitleProps) => {
  const sourceMetadata = getSourceMetadata(connector.source);

  let additionalMetadata = new Map<string, string>();

  const mainSectionClassName = "text-blue-500 flex w-fit";
  const mainDisplay = (
    <>
      {sourceMetadata.icon({ size: 20 })}
      <div className="ml-1 my-auto">
        {ccPairName || sourceMetadata.displayName}
      </div>
    </>
  );
  return (
    <div className="my-auto">
      {isLink ? (
        <Link
          className={mainSectionClassName}
          href={`/admin/connector/${ccPairId}`}
        >
          {mainDisplay}
        </Link>
      ) : (
        <div className={mainSectionClassName}>{mainDisplay}</div>
      )}
      {showMetadata && additionalMetadata.size > 0 && (
        <div className="text-xs mt-1">
          {Array.from(additionalMetadata.entries()).map(([key, value]) => {
            return (
              <div key={key}>
                <i>{key}:</i> {value}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
