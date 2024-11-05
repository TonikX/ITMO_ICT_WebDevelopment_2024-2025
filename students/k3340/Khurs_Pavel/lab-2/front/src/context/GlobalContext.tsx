"use client";
import { AuthProvider } from "@/context/AuthContext";
import { NextUIProvider } from "@nextui-org/react";
import { useRouter } from "next/navigation";

import {
  ThemeProvider as NextThemesProvider,
  ThemeProviderProps,
} from "next-themes";

export interface GlobalContextProps {
  children: React.ReactNode;
  themeProps?: ThemeProviderProps;
}

const GlobalContext = ({ children, themeProps }: GlobalContextProps) => {
  const router = useRouter();

  return (
    <NextThemesProvider {...themeProps} defaultTheme="system" enableSystem>
      <NextUIProvider navigate={router.push}>
        <AuthProvider>{children}</AuthProvider>
      </NextUIProvider>
    </NextThemesProvider>
  );
};

export default GlobalContext;
