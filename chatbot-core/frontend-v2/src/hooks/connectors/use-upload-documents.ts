import { useMutation } from '@tanstack/react-query';

import { ReactMutationKey } from '@/constants/react-query-key';
import { uploadDocuments } from '@/services/connectors/upload-documents';

export const useUploadDocuments = () => {
  return useMutation({
    mutationKey: [ReactMutationKey.UPLOAD_CONNECTOR_DOCUMENTS],
    mutationFn: uploadDocuments,
  });
};
