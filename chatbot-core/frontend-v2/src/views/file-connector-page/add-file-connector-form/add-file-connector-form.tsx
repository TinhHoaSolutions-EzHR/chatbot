'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { Plus } from 'lucide-react';
import { FC, useState } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'sonner';
import { z } from 'zod';

import { Button } from '@/components/ui/button';
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';

import { AddFileConnectorProgress } from './add-file-connector-progress';
import { FileDropzone } from './file-dropzone';
import { useCreateConnectorHelper } from './use-create-connector-helper';

const formSchema = z.object({
  connectorName: z.string().min(1, 'Connector name must be left blank.'),
});

export const AddFileConnectorForm: FC = () => {
  const [files, setFiles] = useState<File[]>([]);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      connectorName: '',
    },
  });

  const { createConnector, isError, progress, progressLabel } = useCreateConnectorHelper();

  const onSubmit = (values: z.infer<typeof formSchema>) => {
    if (!files.length) {
      toast.error('Please choose at least 1 file before continuing.');
    }

    createConnector(values.connectorName, files);
  };

  return (
    <>
      <div className="mt-6 border w-full px-12 py-8 rounded-lg bg-[#f9f9f9] shadow-md">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <FormField
              control={form.control}
              name="connectorName"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Connector name</FormLabel>
                  <FormControl>
                    <Input className="bg-white border" {...field} placeholder="Input your connector name..." />
                  </FormControl>
                  <FormDescription>
                    A descriptive name for your connector (i.e. Software engineering design patterns)
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FileDropzone files={files} setFiles={setFiles} />
            <div className="flex justify-end w-full">
              <Button type="submit" size="default" disabled={!files.length}>
                <Plus /> Add new connector
              </Button>
            </div>
          </form>
        </Form>
      </div>
      <AddFileConnectorProgress isError={isError} progress={progress} progressLabel={progressLabel} />
    </>
  );
};
