import { AppSidebar } from "@/components/app-sidebar";
import { ChatAgentSidebar } from "@/components/app-sidebar copy";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import Script from "next/script";

export const experimental_ppr = true;

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {

  return (
    <>
      <Script
        src="https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js"
        strategy="beforeInteractive"
      />
      <SidebarProvider defaultOpen={true}>
        <AppSidebar user={{ email: "guest", id: "guest", image: "", name: "Guest" }} />
        <SidebarInset>{children}</SidebarInset>
        <ChatAgentSidebar user={{ email: "guest", id: "guest", image: "", name: "Guest" }} />
      </SidebarProvider>
    </>
  );
}
