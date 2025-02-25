import {
  Blocks,
  BookOpen,
  ChartNoAxesColumn,
  ChartSpline,
  ClipboardList,
  CloudUpload,
  Cpu,
  CreditCard,
  Database,
  FileSearch,
  FileText,
  Folder,
  Image,
  KeyRound,
  LucideIcon,
  MessageSquareDot,
  Search,
  Settings,
  ShieldCheck,
  User,
  UsersRound,
  Wrench,
} from 'lucide-react';

import { Route } from './misc';

export interface IAdminItemDetail {
  icon: LucideIcon;
  name: string;
  href: Route;
}

interface IAdminSidebarItems {
  label: string;
  items: IAdminItemDetail[];
}

export const ADMIN_ITEM_DETAIL: Record<string, IAdminItemDetail> = {
  [Route.EXISTING_CONNECTORS]: {
    icon: BookOpen,
    name: 'Existing connectors',
    href: Route.EXISTING_CONNECTORS,
  },
  [Route.ADD_CONNECTOR]: {
    icon: CloudUpload,
    name: 'Add connector',
    href: Route.ADD_CONNECTOR,
  },
};

export const SIDEBAR_CHAT_HISTORY = 'chat-history';

export const ADMIN_SIDEBAR_ITEMS: IAdminSidebarItems[] = [
  {
    label: 'Connectors',
    items: [ADMIN_ITEM_DETAIL[Route.EXISTING_CONNECTORS], ADMIN_ITEM_DETAIL[Route.ADD_CONNECTOR]],
  },
  {
    label: 'Document management',
    items: [
      {
        icon: Folder,
        name: 'Document sets',
        href: Route.NOT_SUPPORTED,
      },
      {
        icon: FileSearch,
        name: 'Document explorer',
        href: Route.NOT_SUPPORTED,
      },
      {
        icon: MessageSquareDot,
        name: 'Document feedback',
        href: Route.NOT_SUPPORTED,
      },
    ],
  },
  {
    label: 'Custom assistants',
    items: [
      {
        icon: Blocks,
        name: 'Assistants',
        href: Route.NOT_SUPPORTED,
      },
      {
        icon: Wrench,
        name: 'Tools',
        href: Route.NOT_SUPPORTED,
      },
      {
        icon: ClipboardList,
        name: 'Standard answers',
        href: Route.NOT_SUPPORTED,
      },
    ],
  },
  {
    label: 'Configuration',
    items: [
      {
        icon: Cpu,
        name: 'LLM setups',
        href: Route.NOT_SUPPORTED,
      },
      {
        icon: Search,
        name: 'Search settings',
        href: Route.NOT_SUPPORTED,
      },
      {
        icon: FileText,
        name: 'Document processing',
        href: Route.NOT_SUPPORTED,
      },
    ],
  },
  {
    label: 'User management',
    items: [
      {
        icon: User,
        name: 'Users',
        href: Route.NOT_SUPPORTED,
      },
      {
        icon: UsersRound,
        name: 'Groups',
        href: Route.NOT_SUPPORTED,
      },
      {
        icon: KeyRound,
        name: 'API keys',
        href: Route.NOT_SUPPORTED,
      },
      {
        icon: ShieldCheck,
        name: 'Token rate limits',
        href: Route.NOT_SUPPORTED,
      },
    ],
  },
  {
    label: 'Performance',
    items: [
      {
        icon: ChartSpline,
        name: 'Usage statistics',
        href: Route.NOT_SUPPORTED,
      },
      {
        icon: Database,
        name: 'Query history',
        href: Route.NOT_SUPPORTED,
      },
      {
        icon: ChartNoAxesColumn,
        name: 'Custom analytics',
        href: Route.NOT_SUPPORTED,
      },
    ],
  },
  {
    label: 'Settings',
    items: [
      {
        icon: Settings,
        name: 'Workspace settings',
        href: Route.NOT_SUPPORTED,
      },
      {
        icon: Image,
        name: 'White labeling',
        href: Route.NOT_SUPPORTED,
      },
      {
        icon: CreditCard,
        name: 'Billing',
        href: Route.NOT_SUPPORTED,
      },
    ],
  },
];
