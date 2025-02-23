import { useState } from 'react';
import { toast } from 'sonner';

import { useCreateConnector } from '@/hooks/connectors/use-create-connector';
import { useUploadDocuments } from '@/hooks/connectors/use-upload-documents';

export const useCreateConnectorHelper = () => {
  const [progress, setProgress] = useState<number>(0);
  const [progressLabel, setProgressLabel] = useState('');
  const [isError, setIsError] = useState(false);

  const { mutateAsync: uploadDocuments } = useUploadDocuments();
  const { mutateAsync: createConnector } = useCreateConnector();

  const createConnectorHelper = async (connectorName: string, files: File[]) => {
    try {
      setProgress(33);
      setProgressLabel('Uploading your documents...');
      setIsError(false);

      const filePaths = await uploadDocuments(files, {
        onError() {
          toast.error('Upload documents failed', {
            description: "There's something wrong with your request. Please try again later!",
          });
          setProgressLabel('Upload documents failed. Please try again.');
        },
        onSuccess() {},
      });

      setProgress(66);
      setProgressLabel('Preparing your connector...');

      await createConnector(
        {
          name: connectorName,
          file_paths: filePaths,
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

      setProgress(100);
      setProgressLabel("You're all set.");
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
