import { Outlet } from "react-router";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";

export default function SidebarLayout() {
  return (
    <div>
      <main>
        <SidebarProvider>
          <AppSidebar />
          <SidebarTrigger />

          <Outlet />
        </SidebarProvider>
      </main>
    </div>
  );
}
