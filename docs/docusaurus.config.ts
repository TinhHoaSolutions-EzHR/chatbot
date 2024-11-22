// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

import type * as Preset from '@docusaurus/preset-classic';
import type { Config } from '@docusaurus/types';
import type * as Plugin from '@docusaurus/types/src/plugin';
import type * as OpenApiPlugin from 'docusaurus-plugin-openapi-docs';

const config: Config = {
  title: 'EzHR Chatbot Local Development Guide',
  tagline: 'EzHR Chatbot Documentation',
  url: 'https://ezhrchatbot.pages.dev/',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  staticDirectories: ['static'],

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'TinhHoaSolutions-EzHR', // Usually your GitHub org/username.
  projectName: 'chatbot',

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.ts'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: 'https://github.com/TinhHoaSolutions-EzHR/chatbot/tree/main/docs',
          docItemComponent: '@theme/ApiItem', // Derived from docusaurus-theme-openapi
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: 'https://github.com/TinhHoaSolutions-EzHR/chatbot/tree/main/docs',
          onInlineAuthors: 'ignore',
          onUntruncatedBlogPosts: 'ignore',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    docs: {
      sidebar: {
        hideable: true,
      },
    },
    navbar: {
      title: 'EzHR Chatbot',
      logo: {
        alt: 'EzHR Chatbot Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'intro',
          position: 'left',
          label: 'Local Development Guide',
        },
        { to: '/blog', label: 'Blog', position: 'left' },
        {
          label: 'Chatbot API',
          position: 'left',
          to: '/docs/chatbot-api/sample-backend',
        },
        {
          href: 'https://github.com/TinhHoaSolutions-EzHR/chatbot',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Local Development Guide',
              to: '/docs/intro',
            },
            {
              label: 'Chatbot API',
              to: '/docs/chatbot-api/sample-backend',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/TinhHoaSolutions-EzHR/chatbot',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} EzHR Chatbot.`,
    },
    prism: {
      prism: {
        additionalLanguages: ['ruby', 'csharp', 'php', 'java', 'powershell', 'json', 'bash'],
      },
      languageTabs: [
        {
          highlight: 'python',
          language: 'python',
          logoClass: 'python',
        },
        {
          highlight: 'bash',
          language: 'curl',
          logoClass: 'bash',
        },
        {
          highlight: 'csharp',
          language: 'csharp',
          logoClass: 'csharp',
        },
        {
          highlight: 'go',
          language: 'go',
          logoClass: 'go',
        },
        {
          highlight: 'javascript',
          language: 'nodejs',
          logoClass: 'nodejs',
        },
        {
          highlight: 'ruby',
          language: 'ruby',
          logoClass: 'ruby',
        },
        {
          highlight: 'php',
          language: 'php',
          logoClass: 'php',
        },
        {
          highlight: 'java',
          language: 'java',
          logoClass: 'java',
          variant: 'unirest',
        },
        {
          highlight: 'powershell',
          language: 'powershell',
          logoClass: 'powershell',
        },
      ],
    },
  } satisfies Preset.ThemeConfig,

  plugins: [
    [
      'docusaurus-plugin-openapi-docs',
      {
        id: 'openapi',
        docsPluginId: 'classic',
        config: {
          chatbotApi: {
            specPath: 'static/openapi.yaml',
            outputDir: 'docs/chatbot-api',

            sidebarOptions: {
              groupPathsBy: 'tag',
              categoryLinkSource: 'tag',
            },
          } satisfies OpenApiPlugin.Options,
        } satisfies Plugin.PluginOptions,
      },
    ],
  ],

  themes: ['docusaurus-theme-openapi-docs'],
};

export default async function createConfig() {
  return config;
}
