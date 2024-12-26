export type SiteConfig = typeof siteConfig;

export const siteConfig = {
  name: 'Автобусный парк',
  description: 'Система управления маршрутами, водителями и автобусами.',
  navItems: [
    {
      label: 'Главная',
      href: '/',
    },
    {
      label: 'Водители',
      href: '/drivers',
    },
    {
      label: 'Автобусы',
      href: '/buses',
    },
    {
      label: 'Маршруты',
      href: '/routes',
    },
    {
      label: 'Смены',
      href: '/work-shifts',
    },
  ],
};
