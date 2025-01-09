'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { Loader2 } from 'lucide-react';
import { FC } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'sonner';
import { z } from 'zod';

import { Button } from '@/components/ui/button';
import { DialogFooter } from '@/components/ui/dialog';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { useCreateChatFolder } from '@/hooks/chat/use-create-chat-folder';
import { useDialogStore } from '@/hooks/stores/use-dialog-store';

const formSchema = z.object({
  folderName: z.string().min(1, 'Folder name must not be left blank'),
});

export const CreateChatFolderForm: FC = () => {
  const { closeDialog } = useDialogStore();

  const { mutate, isPending } = useCreateChatFolder();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      folderName: '',
    },
  });

  const onSubmit = (values: z.infer<typeof formSchema>) => {
    mutate(values.folderName, {
      onSuccess() {
        toast.success('Folder created successfully!');
        closeDialog();
      },
      onError() {
        toast.error('Folder created unsuccessfully!', {
          description: 'Please try again later.',
        });
      },
    });
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

        <DialogFooter className="mt-8">
          <div className="flex gap-2">
            <Button type="submit" disabled={isPending}>
              {isPending ? <Loader2 className="animate-spin" size={14} /> : 'Submit'}
            </Button>
            <Button variant="secondary" onClick={closeDialog} disabled={isPending}>
              Cancel
            </Button>
          </div>
        </DialogFooter>
      </form>
    </Form>
  );
};
