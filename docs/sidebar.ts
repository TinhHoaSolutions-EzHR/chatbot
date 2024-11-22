import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebar: SidebarsConfig = {
  introSideBar: [
    {
      type: 'doc',
      id: 'intro',
    },
    {
      type: 'category',
      label: 'Chatbot API',
      items: require('./docs/chatbot-api/sidebar.ts'),
    },
  ],
};

export default sidebar.apisidebar;
