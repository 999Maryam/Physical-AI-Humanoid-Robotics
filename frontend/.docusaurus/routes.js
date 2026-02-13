import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/ur/docs',
    component: ComponentCreator('/ur/docs', 'd95'),
    routes: [
      {
        path: '/ur/docs',
        component: ComponentCreator('/ur/docs', 'a7f'),
        routes: [
          {
            path: '/ur/docs',
            component: ComponentCreator('/ur/docs', 'bc1'),
            routes: [
              {
                path: '/ur/docs/basics-of-humanoid-robotics',
                component: ComponentCreator('/ur/docs/basics-of-humanoid-robotics', '246'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/capstone',
                component: ComponentCreator('/ur/docs/capstone', '47c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/digital-twin-simulation',
                component: ComponentCreator('/ur/docs/digital-twin-simulation', '554'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/introduction-to-physical-ai',
                component: ComponentCreator('/ur/docs/introduction-to-physical-ai', '6da'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/ros-2-fundamentals',
                component: ComponentCreator('/ur/docs/ros-2-fundamentals', '96e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/vision-language-action-5vla',
                component: ComponentCreator('/ur/docs/vision-language-action-5vla', '116'),
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
    path: '/ur/',
    component: ComponentCreator('/ur/', '3b1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
