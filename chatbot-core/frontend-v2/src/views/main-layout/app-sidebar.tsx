import { NewChatButton } from '@/components/new-chat-button';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
  SidebarTrigger,
} from '@/components/ui/sidebar';

export function AppSidebar() {
  return (
    <Sidebar>
      <SidebarHeader>
        <div className="w-full flex justify-between">
          <SidebarTrigger />
          <NewChatButton />
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup />
        <SidebarGroup />
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  );
}
