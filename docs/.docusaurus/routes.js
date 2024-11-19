import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/blog',
    component: ComponentCreator('/blog', '6a3'),
    exact: true
  },
  {
    path: '/blog/A blogpost',
    component: ComponentCreator('/blog/A blogpost', '52b'),
    exact: true
  },
  {
    path: '/blog/archive',
    component: ComponentCreator('/blog/archive', '182'),
    exact: true
  },
  {
    path: '/blog/authors',
    component: ComponentCreator('/blog/authors', '0b7'),
    exact: true
  },
  {
    path: '/blog/authors/lekiet',
    component: ComponentCreator('/blog/authors/lekiet', '01c'),
    exact: true
  },
  {
    path: '/search',
    component: ComponentCreator('/search', '822'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '1f9'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'e8a'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '06b'),
            routes: [
              {
                path: '/docs/category/chatbot-api',
                component: ComponentCreator('/docs/category/chatbot-api', '077'),
                exact: true,
                sidebar: "localDevelopmentGuideSidebar"
              },
              {
                path: '/docs/category/local-development-guide',
                component: ComponentCreator('/docs/category/local-development-guide', '92d'),
                exact: true,
                sidebar: "localDevelopmentGuideSidebar"
              },
              {
                path: '/docs/chatbot-api/admin-google-drive-auth-manage-admin-connector-google-drive-authorize-credential-id-get',
                component: ComponentCreator('/docs/chatbot-api/admin-google-drive-auth-manage-admin-connector-google-drive-authorize-credential-id-get', '170'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/admin-search-admin-search-post',
                component: ComponentCreator('/docs/chatbot-api/admin-search-admin-search-post', 'a50'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/associate-credential-to-connector-manage-connector-connector-id-credential-credential-id-put',
                component: ComponentCreator('/docs/chatbot-api/associate-credential-to-connector-manage-connector-connector-id-credential-credential-id-put', '932'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/auth-database-logout-auth-logout-post',
                component: ComponentCreator('/docs/chatbot-api/auth-database-logout-auth-logout-post', '40c'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/build-final-template-prompt-persona-utils-prompt-explorer-get',
                component: ComponentCreator('/docs/chatbot-api/build-final-template-prompt-persona-utils-prompt-explorer-get', 'e9d'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/cancel-new-embedding-secondary-index-cancel-new-embedding-post',
                component: ComponentCreator('/docs/chatbot-api/cancel-new-embedding-secondary-index-cancel-new-embedding-post', '54a'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/check-drive-tokens-manage-admin-connector-google-drive-check-auth-credential-id-get',
                component: ComponentCreator('/docs/chatbot-api/check-drive-tokens-manage-admin-connector-google-drive-check-auth-credential-id-get', '3d6'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/check-google-app-credentials-exist-manage-admin-connector-google-drive-app-credential-get',
                component: ComponentCreator('/docs/chatbot-api/check-google-app-credentials-exist-manage-admin-connector-google-drive-app-credential-get', '149'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/check-google-app-gmail-credentials-exist-manage-admin-connector-gmail-app-credential-get',
                component: ComponentCreator('/docs/chatbot-api/check-google-app-gmail-credentials-exist-manage-admin-connector-gmail-app-credential-get', '793'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/check-google-service-account-key-exist-manage-admin-connector-google-drive-service-account-key-get',
                component: ComponentCreator('/docs/chatbot-api/check-google-service-account-key-exist-manage-admin-connector-google-drive-service-account-key-get', 'c71'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/check-google-service-gmail-account-key-exist-manage-admin-connector-gmail-service-account-key-get',
                component: ComponentCreator('/docs/chatbot-api/check-google-service-gmail-account-key-exist-manage-admin-connector-gmail-service-account-key-get', 'b76'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/connector-run-once-manage-admin-connector-run-once-post',
                component: ComponentCreator('/docs/chatbot-api/connector-run-once-manage-admin-connector-run-once-post', 'fbc'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/create-api-key-admin-api-key-post',
                component: ComponentCreator('/docs/chatbot-api/create-api-key-admin-api-key-post', '8c9'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/create-chat-feedback-chat-create-chat-message-feedback-post',
                component: ComponentCreator('/docs/chatbot-api/create-chat-feedback-chat-create-chat-message-feedback-post', 'a69'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/create-connector-from-model-manage-admin-connector-post',
                component: ComponentCreator('/docs/chatbot-api/create-connector-from-model-manage-admin-connector-post', '8c8'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/create-credential-from-model-manage-credential-post',
                component: ComponentCreator('/docs/chatbot-api/create-credential-from-model-manage-credential-post', 'cbc'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/create-deletion-attempt-for-connector-id-manage-admin-deletion-attempt-post',
                component: ComponentCreator('/docs/chatbot-api/create-deletion-attempt-for-connector-id-manage-admin-deletion-attempt-post', '7a4'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/create-document-set-manage-admin-document-set-post',
                component: ComponentCreator('/docs/chatbot-api/create-document-set-manage-admin-document-set-post', '3f5'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/create-new-chat-session-chat-create-chat-session-post',
                component: ComponentCreator('/docs/chatbot-api/create-new-chat-session-chat-create-chat-session-post', '9d2'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/create-persona-admin-persona-post',
                component: ComponentCreator('/docs/chatbot-api/create-persona-admin-persona-post', 'ffb'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/create-prompt-prompt-post',
                component: ComponentCreator('/docs/chatbot-api/create-prompt-prompt-post', '29d'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/create-search-feedback-chat-document-search-feedback-post',
                component: ComponentCreator('/docs/chatbot-api/create-search-feedback-chat-document-search-feedback-post', '5f2'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/create-slack-bot-config-manage-admin-slack-bot-config-post',
                component: ComponentCreator('/docs/chatbot-api/create-slack-bot-config-manage-admin-slack-bot-config-post', 'd3d'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/create-user-group-manage-admin-user-group-post',
                component: ComponentCreator('/docs/chatbot-api/create-user-group-manage-admin-user-group-post', '05c'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-api-key-admin-api-key-api-key-id-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-api-key-admin-api-key-api-key-id-delete', '82d'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-chat-session-by-id-chat-delete-chat-session-session-id-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-chat-session-by-id-chat-delete-chat-session-session-id-delete', '8c9'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-connector-by-id-manage-admin-connector-connector-id-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-connector-by-id-manage-admin-connector-connector-id-delete', '821'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-credential-by-id-admin-manage-admin-credential-credential-id-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-credential-by-id-admin-manage-admin-credential-credential-id-delete', 'bda'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-credential-by-id-manage-credential-credential-id-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-credential-by-id-manage-credential-credential-id-delete', 'ad2'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-document-set-manage-admin-document-set-document-set-id-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-document-set-manage-admin-document-set-document-set-id-delete', '591'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-genai-api-key-manage-admin-genai-api-key-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-genai-api-key-manage-admin-genai-api-key-delete', '8b3'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-google-app-credentials-manage-admin-connector-google-drive-app-credential-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-google-app-credentials-manage-admin-connector-google-drive-app-credential-delete', '457'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-google-app-gmail-credentials-manage-admin-connector-gmail-app-credential-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-google-app-gmail-credentials-manage-admin-connector-gmail-app-credential-delete', '109'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-google-service-account-key-manage-admin-connector-google-drive-service-account-key-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-google-service-account-key-manage-admin-connector-google-drive-service-account-key-delete', '841'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-google-service-gmail-account-key-manage-admin-connector-gmail-service-account-key-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-google-service-gmail-account-key-manage-admin-connector-gmail-service-account-key-delete', '604'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-persona-admin-persona-persona-id-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-persona-admin-persona-persona-id-delete', 'c04'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-prompt-prompt-prompt-id-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-prompt-prompt-prompt-id-delete', '3a7'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-slack-bot-config-manage-admin-slack-bot-config-slack-bot-config-id-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-slack-bot-config-manage-admin-slack-bot-config-slack-bot-config-id-delete', 'bd1'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/delete-user-group-manage-admin-user-group-user-group-id-delete',
                component: ComponentCreator('/docs/chatbot-api/delete-user-group-manage-admin-user-group-user-group-id-delete', '133'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/dissociate-credential-from-connector-manage-connector-connector-id-credential-credential-id-delete',
                component: ComponentCreator('/docs/chatbot-api/dissociate-credential-from-connector-manage-connector-connector-id-credential-credential-id-delete', '31e'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/document-boost-update-manage-admin-doc-boosts-post',
                component: ComponentCreator('/docs/chatbot-api/document-boost-update-manage-admin-doc-boosts-post', '239'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/document-hidden-update-manage-admin-doc-hidden-post',
                component: ComponentCreator('/docs/chatbot-api/document-hidden-update-manage-admin-doc-hidden-post', '676'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/document-ingestion-danswer-api-doc-ingestion-post',
                component: ComponentCreator('/docs/chatbot-api/document-ingestion-danswer-api-doc-ingestion-post', '567'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/document-set-public-manage-document-set-public-get',
                component: ComponentCreator('/docs/chatbot-api/document-set-public-manage-document-set-public-get', 'ae6'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-answer-with-quote-query-answer-with-quote-post',
                component: ComponentCreator('/docs/chatbot-api/get-answer-with-quote-query-answer-with-quote-post', '4cf'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-answer-with-quote-query-stream-answer-with-quote-post',
                component: ComponentCreator('/docs/chatbot-api/get-answer-with-quote-query-stream-answer-with-quote-post', 'a65'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-auth-type-auth-type-get',
                component: ComponentCreator('/docs/chatbot-api/get-auth-type-auth-type-get', '4db'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-basic-connector-indexing-status-manage-indexing-status-get',
                component: ComponentCreator('/docs/chatbot-api/get-basic-connector-indexing-status-manage-indexing-status-get', '2f9'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-cc-pair-full-info-manage-admin-cc-pair-cc-pair-id-get',
                component: ComponentCreator('/docs/chatbot-api/get-cc-pair-full-info-manage-admin-cc-pair-cc-pair-id-get', '3be'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-chat-session-admin-admin-chat-session-history-chat-session-id-get',
                component: ComponentCreator('/docs/chatbot-api/get-chat-session-admin-admin-chat-session-history-chat-session-id-get', '013'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-chat-session-chat-get-chat-session-session-id-get',
                component: ComponentCreator('/docs/chatbot-api/get-chat-session-chat-get-chat-session-session-id-get', 'f84'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-chat-session-history-admin-chat-session-history-get',
                component: ComponentCreator('/docs/chatbot-api/get-chat-session-history-admin-chat-session-history-get', 'd64'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-chunk-info-document-chunk-info-get',
                component: ComponentCreator('/docs/chatbot-api/get-chunk-info-document-chunk-info-get', '4f0'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-connector-by-id-manage-connector-connector-id-get',
                component: ComponentCreator('/docs/chatbot-api/get-connector-by-id-manage-connector-connector-id-get', '8d5'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-connector-indexing-status-manage-admin-connector-indexing-status-get',
                component: ComponentCreator('/docs/chatbot-api/get-connector-indexing-status-manage-admin-connector-indexing-status-get', '417'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-connectors-manage-connector-get',
                component: ComponentCreator('/docs/chatbot-api/get-connectors-manage-connector-get', '960'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-credential-by-id-manage-credential-credential-id-get',
                component: ComponentCreator('/docs/chatbot-api/get-credential-by-id-manage-credential-credential-id-get', 'd5c'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-current-embedding-model-secondary-index-get-current-embedding-model-get',
                component: ComponentCreator('/docs/chatbot-api/get-current-embedding-model-secondary-index-get-current-embedding-model-get', '208'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-default-model-admin-persona-utils-default-model-get',
                component: ComponentCreator('/docs/chatbot-api/get-default-model-admin-persona-utils-default-model-get', '0ee'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-document-info-document-document-size-info-get',
                component: ComponentCreator('/docs/chatbot-api/get-document-info-document-document-size-info-get', '6f3'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-embedding-models-secondary-index-get-embedding-models-get',
                component: ComponentCreator('/docs/chatbot-api/get-embedding-models-secondary-index-get-embedding-models-get', '9f0'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-gen-ai-api-key-from-dynamic-config-store-manage-admin-genai-api-key-get',
                component: ComponentCreator('/docs/chatbot-api/get-gen-ai-api-key-from-dynamic-config-store-manage-admin-genai-api-key-get', 'ed3'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-max-document-tokens-chat-max-selected-document-tokens-get',
                component: ComponentCreator('/docs/chatbot-api/get-max-document-tokens-chat-max-selected-document-tokens-get', 'fb1'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-most-boosted-docs-manage-admin-doc-boosts-get',
                component: ComponentCreator('/docs/chatbot-api/get-most-boosted-docs-manage-admin-doc-boosts-get', '262'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-persona-persona-persona-id-get',
                component: ComponentCreator('/docs/chatbot-api/get-persona-persona-persona-id-get', '070'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-prompt-prompt-prompt-id-get',
                component: ComponentCreator('/docs/chatbot-api/get-prompt-prompt-prompt-id-get', 'b6b'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-query-analytics-analytics-admin-query-get',
                component: ComponentCreator('/docs/chatbot-api/get-query-analytics-analytics-admin-query-get', 'b4f'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-query-history-as-csv-admin-query-history-csv-get',
                component: ComponentCreator('/docs/chatbot-api/get-query-history-as-csv-admin-query-history-csv-get', '94b'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-search-type-query-search-intent-post',
                component: ComponentCreator('/docs/chatbot-api/get-search-type-query-search-intent-post', '345'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-secondary-embedding-model-secondary-index-get-secondary-embedding-model-get',
                component: ComponentCreator('/docs/chatbot-api/get-secondary-embedding-model-secondary-index-get-secondary-embedding-model-get', 'dca'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-tags-query-valid-tags-get',
                component: ComponentCreator('/docs/chatbot-api/get-tags-query-valid-tags-get', '660'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-tokens-manage-admin-slack-bot-tokens-get',
                component: ComponentCreator('/docs/chatbot-api/get-tokens-manage-admin-slack-bot-tokens-get', 'a51'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-user-analytics-analytics-admin-user-get',
                component: ComponentCreator('/docs/chatbot-api/get-user-analytics-analytics-admin-user-get', 'e6e'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-user-chat-sessions-chat-get-user-chat-sessions-get',
                component: ComponentCreator('/docs/chatbot-api/get-user-chat-sessions-chat-get-user-chat-sessions-get', 'a58'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-user-role-manage-get-user-role-get',
                component: ComponentCreator('/docs/chatbot-api/get-user-role-manage-get-user-role-get', '2fa'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/get-version-version-get',
                component: ComponentCreator('/docs/chatbot-api/get-version-version-get', '68c'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/gmail-auth-manage-connector-gmail-authorize-credential-id-get',
                component: ComponentCreator('/docs/chatbot-api/gmail-auth-manage-connector-gmail-authorize-credential-id-get', 'd42'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/gmail-callback-manage-connector-gmail-callback-get',
                component: ComponentCreator('/docs/chatbot-api/gmail-callback-manage-connector-gmail-callback-get', '9ca'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/google-drive-auth-manage-connector-google-drive-authorize-credential-id-get',
                component: ComponentCreator('/docs/chatbot-api/google-drive-auth-manage-connector-google-drive-authorize-credential-id-get', '534'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/google-drive-callback-manage-connector-google-drive-callback-get',
                component: ComponentCreator('/docs/chatbot-api/google-drive-callback-manage-connector-google-drive-callback-get', '2c2'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/gpt-search-gpts-gpt-document-search-post',
                component: ComponentCreator('/docs/chatbot-api/gpt-search-gpts-gpt-document-search-post', 'f6e'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/handle-new-chat-message-chat-send-message-post',
                component: ComponentCreator('/docs/chatbot-api/handle-new-chat-message-chat-send-message-post', '699'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/handle-search-request-query-document-search-post',
                component: ComponentCreator('/docs/chatbot-api/handle-search-request-query-document-search-post', 'a06'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/handle-simplified-chat-message-chat-send-message-simple-api-post',
                component: ComponentCreator('/docs/chatbot-api/handle-simplified-chat-message-chat-send-message-simple-api-post', 'bd6'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/healthcheck-health-get',
                component: ComponentCreator('/docs/chatbot-api/healthcheck-health-get', 'fc3'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/list-all-users-manage-users-get',
                component: ComponentCreator('/docs/chatbot-api/list-all-users-manage-users-get', 'd67'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/list-api-keys-admin-api-key-get',
                component: ComponentCreator('/docs/chatbot-api/list-api-keys-admin-api-key-get', 'c0c'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/list-available-model-versions-admin-persona-utils-list-available-models-get',
                component: ComponentCreator('/docs/chatbot-api/list-available-model-versions-admin-persona-utils-list-available-models-get', 'a46'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/list-credentials-admin-manage-admin-credential-get',
                component: ComponentCreator('/docs/chatbot-api/list-credentials-admin-manage-admin-credential-get', '0c3'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/list-credentials-manage-credential-get',
                component: ComponentCreator('/docs/chatbot-api/list-credentials-manage-credential-get', '35f'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/list-document-sets-manage-document-set-get',
                component: ComponentCreator('/docs/chatbot-api/list-document-sets-manage-document-set-get', '344'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/list-personas-persona-get',
                component: ComponentCreator('/docs/chatbot-api/list-personas-persona-get', '01a'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/list-prompts-prompt-get',
                component: ComponentCreator('/docs/chatbot-api/list-prompts-prompt-get', '5c7'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/list-slack-bot-configs-manage-admin-slack-bot-config-get',
                component: ComponentCreator('/docs/chatbot-api/list-slack-bot-configs-manage-admin-slack-bot-config-get', 'd8d'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/list-user-groups-manage-admin-user-group-get',
                component: ComponentCreator('/docs/chatbot-api/list-user-groups-manage-admin-user-group-get', 'c50'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/oauth-google-database-authorize-auth-oauth-authorize-get',
                component: ComponentCreator('/docs/chatbot-api/oauth-google-database-authorize-auth-oauth-authorize-get', '650'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/oauth-google-database-callback-auth-oauth-callback-get',
                component: ComponentCreator('/docs/chatbot-api/oauth-google-database-callback-auth-oauth-callback-get', 'ecd'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/patch-document-set-manage-admin-document-set-patch',
                component: ComponentCreator('/docs/chatbot-api/patch-document-set-manage-admin-document-set-patch', 'e7f'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/patch-persona-display-priority-admin-persona-display-priority-put',
                component: ComponentCreator('/docs/chatbot-api/patch-persona-display-priority-admin-persona-display-priority-put', '588'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/patch-persona-visibility-admin-persona-persona-id-visible-patch',
                component: ComponentCreator('/docs/chatbot-api/patch-persona-visibility-admin-persona-persona-id-visible-patch', '9e5'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/patch-slack-bot-config-manage-admin-slack-bot-config-slack-bot-config-id-patch',
                component: ComponentCreator('/docs/chatbot-api/patch-slack-bot-config-manage-admin-slack-bot-config-slack-bot-config-id-patch', 'abe'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/patch-user-group-manage-admin-user-group-user-group-id-patch',
                component: ComponentCreator('/docs/chatbot-api/patch-user-group-manage-admin-user-group-user-group-id-patch', 'fe5'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/promote-admin-manage-promote-user-to-admin-patch',
                component: ComponentCreator('/docs/chatbot-api/promote-admin-manage-promote-user-to-admin-patch', 'cac'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/put-tokens-manage-admin-slack-bot-tokens-put',
                component: ComponentCreator('/docs/chatbot-api/put-tokens-manage-admin-slack-bot-tokens-put', '6ae'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/query-validation-query-query-validation-post',
                component: ComponentCreator('/docs/chatbot-api/query-validation-query-query-validation-post', '6bf'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/regenerate-existing-api-key-admin-api-key-api-key-id-patch',
                component: ComponentCreator('/docs/chatbot-api/regenerate-existing-api-key-admin-api-key-api-key-id-patch', '4fa'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/rename-chat-session-chat-rename-chat-session-put',
                component: ComponentCreator('/docs/chatbot-api/rename-chat-session-chat-rename-chat-session-put', '570'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/sample-backend',
                component: ComponentCreator('/docs/chatbot-api/sample-backend', '438'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/set-message-as-latest-chat-set-message-as-latest-put',
                component: ComponentCreator('/docs/chatbot-api/set-message-as-latest-chat-set-message-as-latest-put', '9ab'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/set-new-embedding-model-secondary-index-set-new-embedding-model-post',
                component: ComponentCreator('/docs/chatbot-api/set-new-embedding-model-secondary-index-set-new-embedding-model-post', 'ce3'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/store-genai-api-key-manage-admin-genai-api-key-put',
                component: ComponentCreator('/docs/chatbot-api/store-genai-api-key-manage-admin-genai-api-key-put', '243'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/stream-query-validation-query-stream-query-validation-post',
                component: ComponentCreator('/docs/chatbot-api/stream-query-validation-query-stream-query-validation-post', '08b'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/update-connector-from-model-manage-admin-connector-connector-id-patch',
                component: ComponentCreator('/docs/chatbot-api/update-connector-from-model-manage-admin-connector-connector-id-patch', '387'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/update-credential-from-model-manage-credential-credential-id-patch',
                component: ComponentCreator('/docs/chatbot-api/update-credential-from-model-manage-credential-credential-id-patch', 'f4e'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/update-persona-admin-persona-persona-id-patch',
                component: ComponentCreator('/docs/chatbot-api/update-persona-admin-persona-persona-id-patch', '2e7'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/update-prompt-prompt-prompt-id-patch',
                component: ComponentCreator('/docs/chatbot-api/update-prompt-prompt-prompt-id-patch', '8e6'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/upload-files-manage-admin-connector-file-upload-post',
                component: ComponentCreator('/docs/chatbot-api/upload-files-manage-admin-connector-file-upload-post', '963'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/upsert-gmail-service-account-credential-manage-admin-connector-gmail-service-account-credential-put',
                component: ComponentCreator('/docs/chatbot-api/upsert-gmail-service-account-credential-manage-admin-connector-gmail-service-account-credential-put', '029'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/upsert-google-app-credentials-manage-admin-connector-google-drive-app-credential-put',
                component: ComponentCreator('/docs/chatbot-api/upsert-google-app-credentials-manage-admin-connector-google-drive-app-credential-put', '4de'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/upsert-google-app-gmail-credentials-manage-admin-connector-gmail-app-credential-put',
                component: ComponentCreator('/docs/chatbot-api/upsert-google-app-gmail-credentials-manage-admin-connector-gmail-app-credential-put', '545'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/upsert-google-service-account-key-manage-admin-connector-google-drive-service-account-key-put',
                component: ComponentCreator('/docs/chatbot-api/upsert-google-service-account-key-manage-admin-connector-google-drive-service-account-key-put', '62b'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/upsert-google-service-gmail-account-key-manage-admin-connector-gmail-service-account-key-put',
                component: ComponentCreator('/docs/chatbot-api/upsert-google-service-gmail-account-key-manage-admin-connector-gmail-service-account-key-put', 'd48'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/upsert-service-account-credential-manage-admin-connector-google-drive-service-account-credential-put',
                component: ComponentCreator('/docs/chatbot-api/upsert-service-account-credential-manage-admin-connector-google-drive-service-account-credential-put', '32c'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/validate-existing-genai-api-key-manage-admin-genai-api-key-validate-get',
                component: ComponentCreator('/docs/chatbot-api/validate-existing-genai-api-key-manage-admin-genai-api-key-validate-get', '927'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/chatbot-api/verify-user-logged-in-manage-me-get',
                component: ComponentCreator('/docs/chatbot-api/verify-user-logged-in-manage-me-get', '037'),
                exact: true,
                sidebar: "chatbotApiSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', 'e42'),
                exact: true,
                sidebar: "localDevelopmentGuideSidebar"
              },
              {
                path: '/docs/localDevelopmentGuide/highLevelArchitecture',
                component: ComponentCreator('/docs/localDevelopmentGuide/highLevelArchitecture', '3ea'),
                exact: true,
                sidebar: "localDevelopmentGuideSidebar"
              },
              {
                path: '/docs/localDevelopmentGuide/namingConvention',
                component: ComponentCreator('/docs/localDevelopmentGuide/namingConvention', 'd35'),
                exact: true,
                sidebar: "localDevelopmentGuideSidebar"
              },
              {
                path: '/docs/localDevelopmentGuide/roadmap',
                component: ComponentCreator('/docs/localDevelopmentGuide/roadmap', '566'),
                exact: true,
                sidebar: "localDevelopmentGuideSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '2bc'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
