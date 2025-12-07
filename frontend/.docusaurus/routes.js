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
    path: '/docs',
    component: ComponentCreator('/docs', '604'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'ebf'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '070'),
            routes: [
              {
                path: '/docs/basics-of-humanoid-robotics',
                component: ComponentCreator('/docs/basics-of-humanoid-robotics', '880'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/capstone',
                component: ComponentCreator('/docs/capstone', '5dc'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/digital-twin-simulation',
                component: ComponentCreator('/docs/digital-twin-simulation', '282'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/introduction-to-physical-ai',
                component: ComponentCreator('/docs/introduction-to-physical-ai', '98a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ros-2-fundamentals',
                component: ComponentCreator('/docs/ros-2-fundamentals', 'fd8'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vision-language-action-systems',
                component: ComponentCreator('/docs/vision-language-action-systems', 'e2a'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '2e1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
