export type SiteConfig = typeof siteConfig;

export const siteConfig = {
  name: "Next.js + NextUI",
  description: "Make beautiful websites regardless of your design experience.",
  navItems: [
    {
      label: "Мои брони",
      href: "/reservations",
      isVisibleWithoutAuth: false,
    },
    {
      label: "Продажи",
      href: "/sales",
      isVisibleWithoutAuth: false,
    },
    {
      label: "Туры",
      href: "/tours",
      isVisibleWithoutAuth: false,
    },
    {
      label: "Вход / Регистрация",
      href: "/authentication",
      isVisibleWithoutAuth: true,
    },
  ],
};
