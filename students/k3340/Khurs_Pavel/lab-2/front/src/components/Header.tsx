"use client";
import {
  Navbar as NextUINavbar,
  NavbarContent,
  NavbarMenu,
  NavbarMenuToggle,
  NavbarBrand,
  NavbarItem,
  NavbarMenuItem,
} from "@nextui-org/navbar";
import { Link } from "@nextui-org/link";
import { link as linkStyles } from "@nextui-org/theme";
import NextLink from "next/link";
import clsx from "clsx";
import { siteConfig } from "@/config/siteConfig";
import { useAuth } from "@/context/AuthContext";
import { ThemeSwitch } from "@/components/ThemeSwitch";
import UserDropdown from "@/components/userDropdown";

export default function Header() {
  const { user } = useAuth();

  return (
    <NextUINavbar maxWidth="xl" position="sticky">
      <NavbarContent className="basis-1/5 sm:basis-full" justify="start">
        <NavbarBrand as="li" className="gap-3 max-w-fit">
          <NextLink className="flex justify-start items-center gap-1" href="/">
            <p className="font-bold text-inherit text-foreground-900 uppercase">
              tour agency
            </p>
          </NextLink>
        </NavbarBrand>

        <ul className="hidden sm:flex gap-4 justify-start ml-2">
          {siteConfig.navItems.map(
            (item) =>
              !item.isVisibleWithoutAuth &&
              user && (
                <NavbarItem key={item.href}>
                  <NextLink
                    className={clsx(
                      linkStyles({ color: "foreground" }),
                      "data-[active=true]:text-primary data-[active=true]:font-medium"
                    )}
                    color="foreground"
                    href={item.href}
                  >
                    {item.label}
                  </NextLink>
                </NavbarItem>
              )
          )}
        </ul>
      </NavbarContent>

      <NavbarContent
        className="hidden sm:flex basis-1/5 sm:basis-full"
        justify="end"
      >
        <NavbarItem className="hidden sm:flex gap-2">
          <ThemeSwitch />
          {user && <UserDropdown email={user.email} />}
        </NavbarItem>
      </NavbarContent>

      <NavbarContent className="sm:hidden basis-1 pl-4" justify="end">
        <ThemeSwitch />
        {user && <NavbarMenuToggle />}
      </NavbarContent>

      <NavbarMenu>
        <div className="mx-4 mt-2 flex flex-col gap-2">
          {user && <UserDropdown email={user.email} />}
          {siteConfig.navItems.map(
            (item, index) =>
              !item.isVisibleWithoutAuth &&
              user && (
                <NavbarMenuItem key={`${item}-${index}`}>
                  <Link color={"foreground"} href={item.href} size="lg">
                    {item.label}
                  </Link>
                </NavbarMenuItem>
              )
          )}
        </div>
      </NavbarMenu>
    </NextUINavbar>
  );
}
