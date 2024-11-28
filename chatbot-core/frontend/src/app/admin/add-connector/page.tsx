"use client";
import { SourceIcon } from "@/components/SourceIcon";
import { AdminPageTitle } from "@/components/admin/Title";
import {ConnectorIcon, FileIcon} from "@/components/icons/icons";
import { SourceCategory, SourceMetadata } from "@/lib/search/interfaces";
import Title from "@/components/ui/title";
import { Button } from "@/components/ui/button";
import Link from "next/link";


function SourceTile({
  sourceMetadata,
  preSelect,
}: {
  sourceMetadata: SourceMetadata;
  preSelect?: boolean;
}) {
  return (
    <Link
      className={`flex 
        flex-col 
        items-center 
        justify-center 
        p-4 
        rounded-lg 
        w-40 
        cursor-pointer
        shadow-md
        hover:bg-hover
        ${preSelect ? "bg-hover subtle-pulse" : "bg-hover-light"}
      `}
      href={sourceMetadata.adminUrl}
    >
      <SourceIcon sourceType={sourceMetadata.internalName} iconSize={24} />
      <p className="font-medium text-sm mt-2">{sourceMetadata.displayName}</p>
    </Link>
  );
}
export default function Page() {
  const srcmetadata :SourceMetadata = {
    icon: FileIcon,
    displayName: "File",
    category: SourceCategory.Storage,
    internalName: "file",
    adminUrl: "/admin/connectors/file",
  };

  return (
    <div className="mx-auto container">
      <AdminPageTitle
        icon={<ConnectorIcon size={32} />}
        title="Add Connector"
        farRightElement={
          <Link href="/admin/indexing/status">
            <Button variant="success-reverse">See Connectors</Button>
          </Link>
        }
      />

      <div key="Storage" className="mb-8">
        <div className="flex mt-8">
          <Title>Storage</Title>
        </div>
        <div className="flex flex-wrap gap-4 p-4">
        <SourceTile
          preSelect={
            0 == 0 && 0 == 0
          }
          key="Storage"
          sourceMetadata={srcmetadata}
            />
        </div>
      </div>
    </div>
  );
}
