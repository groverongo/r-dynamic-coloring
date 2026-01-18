import { AgentChatSidebar } from "@/components/AgentChat/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { Providers } from "@/components/providers";
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
      <Providers>
        <SidebarProvider defaultOpen={true}>
          <AppSidebar user={{ email: "guest", id: "guest", image: "", name: "Guest" }} />
          <SidebarInset>{children}</SidebarInset>
          <AgentChatSidebar />
        </SidebarProvider>
      </Providers>
    </>
  );
}
