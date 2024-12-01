import { FileIcon } from "@/components/icons/icons";
import { ValidSources } from "./types";
import { SourceCategory, SourceMetadata } from "./search/interfaces";
import { Persona } from "@/app/admin/assistants/interfaces";

interface PartialSourceMetadata {
  icon: React.FC<{ size?: number; className?: string }>;
  displayName: string;
  category: SourceCategory;
  docs?: string;
}

type SourceMap = {
  [K in ValidSources]: PartialSourceMetadata;
};

const SOURCE_METADATA_MAP: SourceMap = {
  file: {
    icon: FileIcon,
    displayName: "File",
    category: SourceCategory.Storage,
    docs: "https://docs.danswer.dev/connectors/file",
  },

} as SourceMap;

function fillSourceMetadata(
  partialMetadata: PartialSourceMetadata,
  internalName: ValidSources
): SourceMetadata {
  return {
    internalName: internalName,
    ...partialMetadata,
    adminUrl: `/admin/connectors/${internalName}`,
  };
}

export function getSourceMetadata(sourceType: ValidSources): SourceMetadata {
  const response = fillSourceMetadata(
    SOURCE_METADATA_MAP[sourceType],
    sourceType
  );

  return response;
}

export function listSourceMetadata(): SourceMetadata[] {
  /* This gives back all the viewable / common sources, primarily for 
      display in the Add Connector page */
  const entries = Object.entries(SOURCE_METADATA_MAP)
    .filter(
      ([source, _]) => source !== "not_applicable" && source != "ingestion_api"
    )
    .map(([source, metadata]) => {
      return fillSourceMetadata(metadata, source as ValidSources);
    });
  return entries;
}

export function getSourceDocLink(sourceType: ValidSources): string | null {
  return SOURCE_METADATA_MAP[sourceType].docs || null;
}

export const isValidSource = (sourceType: string) => {
  return Object.keys(SOURCE_METADATA_MAP).includes(sourceType);
};

export function getSourceDisplayName(sourceType: ValidSources): string | null {
  return getSourceMetadata(sourceType).displayName;
}

export function getSourceMetadataForSources(sources: ValidSources[]) {
  return sources.map((source) => getSourceMetadata(source));
}

export function getSourcesForPersona(persona: Persona): ValidSources[] {
  const personaSources: ValidSources[] = [];
  persona.document_sets.forEach((documentSet) => {
    documentSet.cc_pair_descriptors.forEach((ccPair) => {
      if (!personaSources.includes(ccPair.connector.source)) {
        personaSources.push(ccPair.connector.source);
      }
    });
  });
  return personaSources;
}
