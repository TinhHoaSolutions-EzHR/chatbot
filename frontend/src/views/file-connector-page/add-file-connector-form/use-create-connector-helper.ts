import { useQueryClient } from '@tanstack/react-query';
import { useState } from 'react';
import { toast } from 'sonner';

import { ReactQueryKey } from '@/constants/react-query-key';
import { useCreateConnector } from '@/hooks/connectors/use-create-connector';
import { useUploadDocuments } from '@/hooks/documents/use-upload-documents';
import { useIndexStore } from '@/hooks/stores/use-index-store';

export const useCreateConnectorHelper = () => {
  const [progress, setProgress] = useState<number>(0);
  const [progressLabel, setProgressLabel] = useState('');
  const [isError, setIsError] = useState(false);

  const queryClient = useQueryClient();

  const addConnector = useIndexStore(state => state.addConnector);

  const { mutateAsync: uploadDocuments } = useUploadDocuments();
  const { mutateAsync: createConnector } = useCreateConnector();

  const createConnectorHelper = async (connectorName: string, files: File[], issueDate: Date) => {
    try {
      setProgress(33);
      setProgressLabel('Uploading your documents...');
      setIsError(false);

      const documents = await uploadDocuments(
        {
          documents: files,
          issueDate,
        },
        {
          onError() {
            toast.error('Upload documents failed', {
              description: "There's something wrong with your request. Please try again later!",
            });
            setProgressLabel('Upload documents failed. Please try again.');
          },
          onSuccess() {},
        },
      );

      setProgress(66);
      setProgressLabel('Preparing your connector...');

      const connector = await createConnector(
        {
          name: connectorName,
          file_paths: documents.map(({ document_url }) => document_url),
        },
        {
          onError() {
            toast.error('Create connector failed', {
              description: "There's something wrong with your request. Please try again later!",
            });
            setProgressLabel('Create connector failed. Please try again.');
          },
        },
      );

      // TODO: Remove this in the future, since get all connectors will also return
      // all task_id
      addConnector(connector.id, documents[0].task_id);

      setProgress(100);
      setProgressLabel("You're all set.");
      queryClient.invalidateQueries({
        queryKey: [ReactQueryKey.CONNECTORS],
        refetchType: 'all',
      });
    } catch {
      setIsError(true);
      return;
    }
  };

  return {
    createConnector: createConnectorHelper,
    progress,
    progressLabel,
    isError,
  };
};
