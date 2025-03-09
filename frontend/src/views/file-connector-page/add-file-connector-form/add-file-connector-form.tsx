'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { format } from 'date-fns';
import { CalendarIcon, Plus } from 'lucide-react';
import { FC, useState } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'sonner';
import { z } from 'zod';

import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { cn } from '@/lib/utils';

import { AddFileConnectorProgress } from './add-file-connector-progress';
import { FileDropzone } from './file-dropzone';
import { useCreateConnectorHelper } from './use-create-connector-helper';

const formSchema = z.object({
  connectorName: z.string().min(1, 'Connector name must not be left blank.'),
  issueDate: z.date({
    required_error: 'Issue date must not be left blank.',
  }),
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

    createConnector(values.connectorName, files, values.issueDate);
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
            <FormField
              control={form.control}
              name="issueDate"
              render={({ field }) => (
                <FormItem className="flex flex-col">
                  <FormLabel>Issue date</FormLabel>
                  <Popover>
                    <PopoverTrigger asChild>
                      <FormControl>
                        <Button
                          variant={'outline'}
                          className={cn(
                            'w-[240px] pl-3 text-left font-normal',
                            !field.value && 'text-muted-foreground',
                          )}
                        >
                          {field.value ? format(field.value, 'PPP') : <span>Pick a date</span>}
                          <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                        </Button>
                      </FormControl>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0" align="start">
                      <Calendar mode="single" selected={field.value} onSelect={field.onChange} />
                    </PopoverContent>
                  </Popover>
                  <FormDescription>
                    The date the document was published (i.e. the date of the first issue)
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
