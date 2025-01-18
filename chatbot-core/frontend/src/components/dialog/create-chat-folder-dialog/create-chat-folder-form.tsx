'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { FC, ReactNode } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';

const formSchema = z.object({
  folderName: z.string().min(1, 'Folder name must not be left blank'),
});

interface ICreateChatFolderFormProps {
  onCreateChatFolder(folderName: string): void;
  children: ReactNode;
}

export const CreateChatFolderForm: FC<ICreateChatFolderFormProps> = ({ onCreateChatFolder, children }) => {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      folderName: '',
    },
  });

  const onSubmit = (values: z.infer<typeof formSchema>) => {
    onCreateChatFolder(values.folderName);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name="folderName"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Folder name</FormLabel>
              <FormControl>
                <Input placeholder="i.e. Growth path in the company" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        {children}
      </form>
    </Form>
  );
};
