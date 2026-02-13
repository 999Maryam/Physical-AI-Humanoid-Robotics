import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/docs',
    component: ComponentCreator('/docs', '0a9'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '0a6'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', 'f22'),
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
                path: '/docs/vision-language-action-5vla',
                component: ComponentCreator('/docs/vision-language-action-5vla', 'a7a'),
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
