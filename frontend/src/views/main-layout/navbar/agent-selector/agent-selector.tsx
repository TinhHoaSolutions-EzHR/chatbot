'use client';

import { useState } from 'react';

import { DropdownMenu, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Sheet, SheetTrigger } from '@/components/ui/sheet';
import WillRender from '@/components/will-render';
import { useGetAgentsList } from '@/hooks/agents/use-get-agents-list';
import { useGetSelectedAgent } from '@/hooks/agents/use-get-selected-agent';
import { useIsMobile } from '@/hooks/use-mobile';

import { AgentSelectorButton } from './agent-selector-button';
import { AgentSelectorDropdown } from './agent-selector-dropdown';
import { AgentSelectorSheet } from './agent-selector-sheet';

export const AgentSelector = () => {
  const { isLoading: isLoadingAgentsList } = useGetAgentsList();
  const selectedAgent = useGetSelectedAgent();

  const [isAgentSelectorOpen, setIsAgentSelectorOpen] = useState(false);
  const isMobile = useIsMobile();

  const onOpenChange = (isOpen: boolean) => {
    // Prevent user from opening the agent selector if the agent list is still loading
    if (!selectedAgent || isLoadingAgentsList) {
      return;
    }

    setIsAgentSelectorOpen(isOpen);
  };

  return (
    <WillRender>
      <WillRender.If when={isMobile}>
        <Sheet open={isAgentSelectorOpen} onOpenChange={onOpenChange}>
          <SheetTrigger asChild>
            <div>
              <AgentSelectorButton isAgentSelectorOpen={isAgentSelectorOpen} />
            </div>
          </SheetTrigger>
          <AgentSelectorSheet />
        </Sheet>
      </WillRender.If>
      <WillRender.Else>
        <DropdownMenu open={isAgentSelectorOpen} onOpenChange={onOpenChange}>
          <DropdownMenuTrigger asChild>
            <div>
              <AgentSelectorButton isAgentSelectorOpen={isAgentSelectorOpen} />
            </div>
          </DropdownMenuTrigger>
          <AgentSelectorDropdown />
        </DropdownMenu>
      </WillRender.Else>
    </WillRender>
  );
};
