// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Runoff Depth Calculator Workshop',
  tagline: 'Build a Tethys Component App step by step',
  favicon: 'img/favicon.ico',

  url: 'https://tethysplatform.github.io',
  baseUrl: '/tethysapp-runoff_depth_calculator/',
  organizationName: 'tethysplatform',
  projectName: 'tethysapp-runoff_depth_calculator',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/', // docs-only mode: docs served at site root
          sidebarPath: './sidebars.js',
          editUrl:
            'https://github.com/tethysplatform/tethysapp-runoff_depth_calculator/tree/main/workshop/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Runoff Depth Calculator Workshop',
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Tutorial',
          },
          {
            href: 'https://github.com/tethysplatform/tethysapp-runoff_depth_calculator',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Tethys',
            items: [
              {label: 'Tethys Platform Docs', href: 'https://docs.tethysplatform.org'},
              {
                label: 'Components SDK',
                href: 'https://docs.tethysplatform.org/en/latest/tethys_sdk/components.html',
              },
            ],
          },
        ],
        copyright: `Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'bash'],
      },
    }),
};

export default config;
