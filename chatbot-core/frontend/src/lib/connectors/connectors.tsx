import * as Yup from "yup";
import { ConfigurableSources, ValidInputTypes, ValidSources } from "../types";
import { AccessTypeGroupSelectorFormType } from "@/components/admin/connectors/AccessTypeGroupSelector";
import { Credential } from "@/lib/connectors/credentials"; // Import Credential type

export function isLoadState(connector_name: string): boolean {
  // TODO: centralize connector metadata like this somewhere instead of hardcoding it here
  const loadStateConnectors = ["web", "xenforo", "file"];
  if (loadStateConnectors.includes(connector_name)) {
    return true;
  }

  return false;
}

export type InputType =
  | "list"
  | "text"
  | "select"
  | "multiselect"
  | "boolean"
  | "number"
  | "file";

export type StringWithDescription = {
  value: string;
  name: string;
  description?: string;
};

export interface Option {
  label: string | ((currentCredential: Credential<any> | null) => string);
  name: string;
  description?:
    | string
    | ((currentCredential: Credential<any> | null) => string);
  query?: string;
  optional?: boolean;
  hidden?: boolean;
  visibleCondition?: (
    values: any,
    currentCredential: Credential<any> | null
  ) => boolean;
  wrapInCollapsible?: boolean;
}

export interface SelectOption extends Option {
  type: "select";
  options?: StringWithDescription[];
  default?: string;
}

export interface ListOption extends Option {
  type: "list";
  default?: string[];
  transform?: (values: string[]) => string[];
}

export interface TextOption extends Option {
  type: "text";
  default?: string;
  isTextArea?: boolean;
}

export interface NumberOption extends Option {
  type: "number";
  default?: number;
}

export interface BooleanOption extends Option {
  type: "checkbox";
  default?: boolean;
}

export interface FileOption extends Option {
  type: "file";
  default?: string;
}

export interface StringTabOption extends Option {
  type: "string_tab";
  default?: string;
}

export interface TabOption extends Option {
  type: "tab";
  defaultTab?: string;
  tabs: {
    label: string;
    value: string;
    fields: (
      | BooleanOption
      | ListOption
      | TextOption
      | NumberOption
      | SelectOption
      | FileOption
      | StringTabOption
    )[];
  }[];
  default?: [];
}

export interface ConnectionConfiguration {
  description: string;
  subtext?: string;
  values: (
    | BooleanOption
    | ListOption
    | TextOption
    | NumberOption
    | SelectOption
    | FileOption
    | TabOption
  )[];
  advanced_values: (
    | BooleanOption
    | ListOption
    | TextOption
    | NumberOption
    | SelectOption
    | FileOption
    | TabOption
  )[];
  overrideDefaultFreq?: number;
}

export const connectorConfigs: Record<
  ConfigurableSources,
  ConnectionConfiguration
> = {
  file: {
    description: "Configure File connector",
    values: [
      {
        type: "file",
        query: "Enter file locations:",
        label: "File Locations",
        name: "file_locations",
        optional: false,
      },
    ],
    advanced_values: [],
  },
};

export function createConnectorInitialValues(
  connector: ConfigurableSources
): Record<string, any> & AccessTypeGroupSelectorFormType {
  const configuration = connectorConfigs[connector];

  return {
    name: "",
    groups: [],
    access_type: "public",
    ...configuration.values.reduce((acc, field) => {
      if (field.type === "select") {
        acc[field.name] = null;
      } else if (field.type === "list") {
        acc[field.name] = field.default || [];
      } else if (field.type === "checkbox") {
        acc[field.name] = field.default || false;
      } else if (field.default !== undefined) {
        acc[field.name] = field.default;
      }
      return acc;
    }, {} as { [record: string]: any }),
  };
}

export function createConnectorValidationSchema(
  connector: ConfigurableSources
): Yup.ObjectSchema<Record<string, any>> {
  const configuration = connectorConfigs[connector];

  return Yup.object().shape({
    access_type: Yup.string().required("Access Type is required"),
    name: Yup.string().required("Connector Name is required"),
    ...configuration.values.reduce((acc, field) => {
      let schema: any =
        field.type === "select"
          ? Yup.string()
          : field.type === "list"
          ? Yup.array().of(Yup.string())
          : field.type === "checkbox"
          ? Yup.boolean()
          : field.type === "file"
          ? Yup.mixed()
          : Yup.string();

      if (!field.optional) {
        schema = schema.required(`${field.label} is required`);
      }

      acc[field.name] = schema;
      return acc;
    }, {} as Record<string, any>),
    // These are advanced settings
    indexingStart: Yup.string().nullable(),
    pruneFreq: Yup.number().min(0, "Prune frequency must be non-negative"),
    refreshFreq: Yup.number().min(0, "Refresh frequency must be non-negative"),
  });
}

export const defaultPruneFreqDays = 30; // 30 days
export const defaultRefreshFreqMinutes = 30; // 30 minutes

// CONNECTORS
export interface ConnectorBase<T> {
  name: string;
  source: ValidSources;
  input_type: ValidInputTypes;
  connector_specific_config: T;
  refresh_freq: number | null;
  prune_freq: number | null;
  indexing_start: Date | null;
  access_type: string;
  groups?: number[];
}

export interface Connector<T> extends ConnectorBase<T> {
  id: number;
  credential_ids: number[];
  time_created: string;
  time_updated: string;
}

export interface GoogleDriveConfig {
  include_shared_drives?: boolean;
  shared_drive_urls?: string;
  include_my_drives?: boolean;
  my_drive_emails?: string;
  shared_folder_urls?: string;
}

export interface GmailConfig {}

export interface FileConfig {
  file_locations: string[];
}