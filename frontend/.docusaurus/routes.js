import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug/',
    component: ComponentCreator('/__docusaurus/debug/', '546'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config/',
    component: ComponentCreator('/__docusaurus/debug/config/', '8a8'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content/',
    component: ComponentCreator('/__docusaurus/debug/content/', '2da'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData/',
    component: ComponentCreator('/__docusaurus/debug/globalData/', '178'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata/',
    component: ComponentCreator('/__docusaurus/debug/metadata/', 'd6c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry/',
    component: ComponentCreator('/__docusaurus/debug/registry/', '6e3'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes/',
    component: ComponentCreator('/__docusaurus/debug/routes/', 'cab'),
    exact: true
  },
  {
    path: '/docs/',
    component: ComponentCreator('/docs/', 'dba'),
    routes: [
      {
        path: '/docs/',
        component: ComponentCreator('/docs/', '418'),
        routes: [
          {
            path: '/docs/',
            component: ComponentCreator('/docs/', '2df'),
            routes: [
              {
                path: '/docs/basics-of-humanoid-robotics/',
                component: ComponentCreator('/docs/basics-of-humanoid-robotics/', 'db1'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/capstone/',
                component: ComponentCreator('/docs/capstone/', '339'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/digital-twin-simulation/',
                component: ComponentCreator('/docs/digital-twin-simulation/', '1bf'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/introduction-to-physical-ai/',
                component: ComponentCreator('/docs/introduction-to-physical-ai/', '812'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ros-2-fundamentals/',
                component: ComponentCreator('/docs/ros-2-fundamentals/', '6dc'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vision-language-action-5vla/',
                component: ComponentCreator('/docs/vision-language-action-5vla/', 'b8f'),
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
