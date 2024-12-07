// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

import type * as Preset from "@docusaurus/preset-classic";
import type { Config } from "@docusaurus/types";
import type * as Plugin from "@docusaurus/types/src/plugin";
import type * as OpenApiPlugin from "docusaurus-plugin-openapi-docs";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

const ORGANIZATION_NAME = "TinhHoaSolutions-EzHR";
const PROJECT_NAME = "chatbot";

const config: Config = {
  title: "EzHR Chatbot Local Development Guide",
  tagline: "EzHR Chatbot Documentation",
  url: `https://${ORGANIZATION_NAME.toLowerCase()}.github.io`,
  baseUrl: `/${PROJECT_NAME}/`,
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  favicon: "img/favicon.ico",
  staticDirectories: ["static"],

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: ORGANIZATION_NAME,
  projectName: PROJECT_NAME,

  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: require.resolve("./sidebars.ts"),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: `https://github.com/${ORGANIZATION_NAME}/${PROJECT_NAME}/tree/main/docs`,
          docItemComponent: "@theme/ApiItem", // Derived from docusaurus-theme-openapi
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
          breadcrumbs: false,
        },
        blog: false,
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      } satisfies Preset.Options,
    ],
  ],
  stylesheets: [
    {
      href: "https://cdn.jsdelivr.net/npm/katex@0.15.3/dist/katex.min.css",
      type: "text/css",
      integrity:
        "sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM",
      crossorigin: "anonymous",
    },
  ],
  themeConfig: {
    docs: {
      sidebar: {
        hideable: true,
        autoCollapseCategories: true,
      },
    },
    navbar: {
      title: "EzHR Chatbot",
      logo: {
        alt: "EzHR Chatbot Logo",
        src: "img/logo.svg",
      },
      items: [
        {
          type: "doc",
          docId: "intro",
          position: "left",
          label: "API Reference",
        },
        { to: "/blog", label: "Local Development Guide", position: "left" },
        {
          href: "https://github.com/TinhHoaSolutions-EzHR/chatbot",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "API Reference",
          items: [
            {
              label: "API Reference",
              to: "/docs/intro",
            },
          ],
        },
        {
          title: "Local Development Guide",
          items: [
            {
              label: "Local Development Guide",
              to: "/blog",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} EzHR Chatbot.`,
    },
    prism: {
      prism: {
        additionalLanguages: [
          "ruby",
          "csharp",
          "php",
          "java",
          "powershell",
          "json",
          "bash",
        ],
      },
      languageTabs: [
        {
          highlight: "python",
          language: "python",
          logoClass: "python",
        },
        {
          highlight: "bash",
          language: "curl",
          logoClass: "bash",
        },
        {
          highlight: "csharp",
          language: "csharp",
          logoClass: "csharp",
        },
        {
          highlight: "go",
          language: "go",
          logoClass: "go",
        },
        {
          highlight: "javascript",
          language: "nodejs",
          logoClass: "nodejs",
        },
        {
          highlight: "ruby",
          language: "ruby",
          logoClass: "ruby",
        },
        {
          highlight: "php",
          language: "php",
          logoClass: "php",
        },
        {
          highlight: "java",
          language: "java",
          logoClass: "java",
          variant: "unirest",
        },
        {
          highlight: "powershell",
          language: "powershell",
          logoClass: "powershell",
        },
      ],
    },
  } satisfies Preset.ThemeConfig,

  plugins: [
    [
      "docusaurus-plugin-openapi-docs",
      {
        id: "openapi",
        docsPluginId: "classic",
        config: {
          chatbotApi: {
            specPath: "static/openapi.yaml",
            outputDir: "docs/chatbot-api",

            sidebarOptions: {
              groupPathsBy: "tag",
              categoryLinkSource: "tag",
            },
          } satisfies OpenApiPlugin.Options,
        } satisfies Plugin.PluginOptions,
      },
    ],
    [
      "@docusaurus/plugin-content-blog",
      {
        id: "blog",
        path: "blog",
        routeBasePath: "blog",
        blogTitle: "Local Development Guide",
        showReadingTime: true,
        feedOptions: {
          type: "all",
          copyright: `Copyright © ${new Date().getFullYear()} Facebook, Inc.`,
          createFeedItems: async (params) => {
            const { blogPosts, defaultCreateFeedItems, ...rest } = params;
            return defaultCreateFeedItems({
              // keep only the 10 most recent blog posts in the feed
              blogPosts: blogPosts.filter((item, index) => index < 10),
              ...rest,
            });
          },
        },
        onInlineAuthors: "ignore",
        onUntruncatedBlogPosts: "ignore",
      },
    ],
  ],

  themes: ["docusaurus-theme-openapi-docs"],
};

export default async function createConfig() {
  return config;
}
