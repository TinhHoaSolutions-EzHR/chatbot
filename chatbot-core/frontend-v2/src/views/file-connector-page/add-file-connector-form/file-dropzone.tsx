import { Hand } from 'lucide-react';
import { FC, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

import { Label } from '@/components/ui/label';
import { formatPlural } from '@/utils/format-plural';

interface IFileDropzoneProps {
  files: File[];
  setFiles(files: File[]): void;
}

export const FileDropzone: FC<IFileDropzoneProps> = ({ files, setFiles }) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length) {
      setFiles(acceptedFiles);
    }
  }, []);

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <Label>Upload files</Label>
        <div
          {...getRootProps({
            className: 'bg-white border flex items-center justify-center h-32 rounded-md shadow cursor-pointer',
          })}
        >
          <input {...getInputProps()} />
          <p className="text-sm font-semibold flex gap-[6px] items-center">
            <Hand size={14} />
            Drop some files here, or click to select files.
          </p>
        </div>
      </div>
      {!!files.length && (
        <div>
          <Label>
            Selected files ({files.length} {formatPlural(files.length, 'file')} selected)
          </Label>
          <ul className="list-disc list-inside space-y-[2px] mt-2">
            {files.map((file, idx) => (
              <li key={idx} className="text-sm">
                {file.name}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
