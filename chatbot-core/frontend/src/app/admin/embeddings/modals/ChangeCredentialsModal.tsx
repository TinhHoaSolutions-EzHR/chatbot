import React, { useRef, useState } from "react";
import { Modal } from "@/components/Modal";
import { Callout } from "@/components/ui/callout";
import Text from "@/components/ui/text";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/admin/connectors/Field";
import { CloudEmbeddingProvider } from "../../../../components/embedding/interfaces";
import {
  EMBEDDING_PROVIDERS_ADMIN_URL,
  LLM_PROVIDERS_ADMIN_URL,
} from "../../configuration/llm/constants";
import { mutate } from "swr";
import { testEmbedding } from "../pages/utils";

export function ChangeCredentialsModal({
  provider,
  onConfirm,
  onCancel,
  onDeleted,
}: {
  provider: CloudEmbeddingProvider;
  onConfirm: () => void;
  onCancel: () => void;
  onDeleted: () => void;
}) {
  const [apiKey, setApiKey] = useState("");
  const [apiUrl, setApiUrl] = useState("");
  const [modelName, setModelName] = useState("");

  const [testError, setTestError] = useState<string>("");
  const [fileName, setFileName] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [deletionError, setDeletionError] = useState<string>("");

  const clearFileInput = () => {
    setFileName("");
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    setFileName("");

    if (file) {
      setFileName(file.name);
      try {
        setDeletionError("");
        const fileContent = await file.text();
        let jsonContent;
        try {
          jsonContent = JSON.parse(fileContent);
          setApiKey(JSON.stringify(jsonContent));
        } catch (parseError) {
          throw new Error(
            "Failed to parse JSON file. Please ensure it's a valid JSON."
          );
        }
      } catch (error) {
        setTestError(
          error instanceof Error
            ? error.message
            : "An unknown error occurred while processing the file."
        );
        setApiKey("");
        clearFileInput();
      }
    }
  };

  const handleDelete = async () => {
    setDeletionError("");
    setIsProcessing(true);

    try {
      const response = await fetch(
        `${EMBEDDING_PROVIDERS_ADMIN_URL}/${provider.provider_type.toLowerCase()}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        setDeletionError(errorData.detail);
        return;
      }

      mutate(LLM_PROVIDERS_ADMIN_URL);
      onDeleted();
    } catch (error) {
      setDeletionError(
        error instanceof Error ? error.message : "An unknown error occurred"
      );
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSubmit = async () => {
    setTestError("");
    const normalizedProviderType = provider.provider_type
      .toLowerCase()
      .split(" ")[0];

    try {
      const testResponse = await testEmbedding({
        provider_type: normalizedProviderType,
        modelName,
        apiKey,
        apiUrl,
        apiVersion: null,
        deploymentName: null,
      });

      if (!testResponse.ok) {
        const errorMsg = (await testResponse.json()).detail;
        throw new Error(errorMsg);
      }

      const updateResponse = await fetch(EMBEDDING_PROVIDERS_ADMIN_URL, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          provider_type: normalizedProviderType,
          api_key: apiKey,
          api_url: apiUrl,
          is_default_provider: false,
          is_configured: true,
        }),
      });

      if (!updateResponse.ok) {
        const errorData = await updateResponse.json();
        throw new Error(
          errorData.detail ||
            `Failed to update provider- check your ${
              "API key"
            }`
        );
      }

      onConfirm();
    } catch (error) {
      setTestError(
        error instanceof Error ? error.message : "An unknown error occurred"
      );
    }
  };
  return (
    <Modal
      width="max-w-3xl"
      icon={provider.icon}
      title={`Modify your ${provider.provider_type} ${
        "key"
      }`}
      onOutsideClick={onCancel}
    >
      <>
        <Text className="mt-4 font-bold text-lg mb-2">
          You can delete your configuration.
        </Text>
        <Text className="mb-2">
          This is only possible if you have already switched to a different
          embedding type!
        </Text>

        <Button
          className="mr-auto"
          onClick={handleDelete}
          variant="destructive"
        >
          Delete Configuration
        </Button>
        {deletionError && (
          <Callout type="danger" title="Error" className="mt-4">
            {deletionError}
          </Callout>
        )}
      </>
    </Modal>
  );
}
