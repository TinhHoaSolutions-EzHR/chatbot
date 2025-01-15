import { File } from 'lucide-react';

import { AddFileConnectorForm } from './add-file-connector-form/add-file-connector-form';

export default function FileConnectorPage() {
  return (
    <>
      <h1 className="flex items-center gap-2 text-3xl text-zinc-800 font-bold">
        <File size={30} className="text-blue-600" />
        File
      </h1>
      <AddFileConnectorForm />
    </>
  );
}
