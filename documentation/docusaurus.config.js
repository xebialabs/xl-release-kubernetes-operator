const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

module.exports = {
    title: 'Release Kubernetes Operator',
    tagline: '',
    url: 'https://xebialabs.github.io',
    baseUrl: '/xl-release-kubernetes-operator/',
    onBrokenLinks: 'throw',
    onBrokenMarkdownLinks: 'warn',
    favicon: 'img/digital_ai.svg',
    organizationName: 'Digital.ai',
    projectName: 'xl-release-kubernetes-operator',
    themeConfig: {
        navbar: {
            title: 'Release Kubernetes Operator',
            logo: {
                alt: 'Release Kubernetes Operator Digital.ai',
                src: 'img/digital_ai.svg',
            },
            items: [
                {
                    type: 'doc',
                    docId: 'intro',
                    position: 'left',
                    label: 'Tutorial',
                },

                {
                    href: 'https://github.com/xebialabs/xl-release-kubernetes-operator',
                    label: 'GitHub',
                    position: 'right',
                }
            ],
        },
        footer: {
            style: 'dark',
            links: [
                {
                    title: 'Docs',
                    items: [
                        {
                            label: 'Tutorial',
                            to: '/docs/intro',
                        },
                        {
                            label: 'GitHub',
                            href: 'https://github.com/xebialabs/xl-release-kubernetes-operator',
                        },
                    ],
                },
            ],
            copyright: `Copyright © ${new Date().getFullYear()} Release Kubernetes Operator Digital.ai`,
        },
        prism: {
            theme: lightCodeTheme,
            darkTheme: darkCodeTheme,
        },
    },
    presets: [
        [
            '@docusaurus/preset-classic',
            {
                docs: {
                    sidebarPath: require.resolve('./sidebars.js')
                },
                theme: {
                    customCss: require.resolve('./src/css/custom.css'),
                },
            },
        ],
    ],
};
