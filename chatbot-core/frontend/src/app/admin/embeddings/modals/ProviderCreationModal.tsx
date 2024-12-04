import React, { useRef, useState } from "react";
import Text from "@/components/ui/text";
import { Callout } from "@/components/ui/callout";
import { Button } from "@/components/ui/button";
import { Form, Formik } from "formik";
import * as Yup from "yup";
import { TextFormField } from "@/components/admin/connectors/Field";
import { LoadingAnimation } from "@/components/Loading";
import {
  CloudEmbeddingProvider,
  EmbeddingProvider,
} from "@/components/embedding/interfaces";
import { EMBEDDING_PROVIDERS_ADMIN_URL } from "../../configuration/llm/constants";
import { Modal } from "@/components/Modal";

export function ProviderCreationModal({
  selectedProvider,
  onConfirm,
  onCancel,
  existingProvider,
}: {
  updateCurrentModel: (
    newModel: string,
    provider_type: EmbeddingProvider
  ) => void;
  selectedProvider: CloudEmbeddingProvider;
  onConfirm: () => void;
  onCancel: () => void;
  existingProvider?: CloudEmbeddingProvider;
}) {
  const [isProcessing, setIsProcessing] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string>("");
  const initialValues = {
    provider_type:
      existingProvider?.provider_type || selectedProvider.provider_type,
    api_key: existingProvider?.api_key || "",
    api_url: existingProvider?.api_url || "",
    custom_config: existingProvider?.custom_config
      ? Object.entries(existingProvider.custom_config)
      : [],
    model_id: 0,
    model_name: null,
  };

  const validationSchema = Yup.object({
    provider_type: Yup.string().required("Provider type is required"),
    api_key: Yup.string().required("API Key is required"),
    model_name: Yup.string().nullable(),
    api_url: Yup.string(),
    deployment_name: Yup.string(),
    api_version: Yup.string(),
    custom_config: Yup.array().of(Yup.array().of(Yup.string()).length(2)),
  });
  useRef<HTMLInputElement>(null);
  const handleSubmit = async (
    values: any,
    { setSubmitting }: { setSubmitting: (isSubmitting: boolean) => void }
  ) => {
    setIsProcessing(true);
    setErrorMsg("");
    try {
      const customConfig = Object.fromEntries(values.custom_config);
      const providerType = values.provider_type.toLowerCase().split(" ")[0];
      const isOpenAI = providerType === "openai";

      const testModelName = isOpenAI
        ? "text-embedding-3-small"
        : values.model_name;

      const testEmbeddingPayload = {
        provider_type: providerType,
        api_key: values.api_key,
        api_url: values.api_url,
        model_name: testModelName,
        api_version: values.api_version,
        deployment_name: values.deployment_name,
      };

      const initialResponse = await fetch(
        "/api/admin/embedding/test-embedding",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(testEmbeddingPayload),
        }
      );

      if (!initialResponse.ok) {
        const errorMsg = (await initialResponse.json()).detail;
        setErrorMsg(errorMsg);
        setIsProcessing(false);
        setSubmitting(false);
        return;
      }

      const response = await fetch(EMBEDDING_PROVIDERS_ADMIN_URL, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...values,
          api_version: values.api_version,
          deployment_name: values.deployment_name,
          provider_type: values.provider_type.toLowerCase().split(" ")[0],
          custom_config: customConfig,
          is_default_provider: false,
          is_configured: true,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || "Failed to update provider- check your API key"
        );
      }

      onConfirm();
    } catch (error: unknown) {
      if (error instanceof Error) {
        setErrorMsg(error.message);
      } else {
        setErrorMsg("An unknown error occurred");
      }
    } finally {
      setIsProcessing(false);
      setSubmitting(false);
    }
  };

  return (
    <Modal
      title={`Configure ${selectedProvider.provider_type}`}
      onOutsideClick={onCancel}
      icon={selectedProvider.icon}
    >
      <div>
        <Formik
          initialValues={initialValues}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting, handleSubmit }) => (
            <Form onSubmit={handleSubmit} className="space-y-4">
              <Text className="text-lg mb-2">
                You are setting the credentials for this provider. To access
                this information, follow the instructions{" "}
                <a
                  className="cursor-pointer underline"
                  target="_blank"
                  href={selectedProvider.docsLink}
                  rel="noreferrer"
                >
                  here
                </a>{" "}
                and gather your{" "}
                <a
                  className="cursor-pointer underline"
                  target="_blank"
                  href={selectedProvider.apiLink}
                  rel="noreferrer"
                ></a>
              </Text>

              <div className="flex w-full flex-col gap-y-6">
                <TextFormField
                  name="api_key"
                  label={`API Key`}
                  placeholder="API Key"
                  type="password"
                />

                <a
                  href={selectedProvider.apiLink}
                  target="_blank"
                  className="underline cursor-pointer"
                  rel="noreferrer"
                >
                  Learn more here
                </a>
              </div>

              {errorMsg && (
                <Callout title="Error" type="danger">
                  {errorMsg}
                </Callout>
              )}

              <Button
                type="submit"
                variant="submit"
                className="w-full"
                disabled={isSubmitting}
              >
                {isProcessing ? (
                  <LoadingAnimation />
                ) : existingProvider ? (
                  "Update"
                ) : (
                  "Create"
                )}
              </Button>
            </Form>
          )}
        </Formik>
      </div>
    </Modal>
  );
}
