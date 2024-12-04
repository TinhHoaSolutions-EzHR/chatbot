import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebar: SidebarsConfig = {
  introSideBar: [
    {
      type: 'category',
      label: 'Chatbot API',
      items: require('./chatbot-api/sidebar.ts'),
    },
  ],
};

export default sidebar.apisidebar;
