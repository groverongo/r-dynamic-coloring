import type { ComponentProps } from "react";

import { useSidebar, type SidebarTrigger } from "@/components/ui/sidebar";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";
import { PanelLeft, PanelRight } from "lucide-react";
import { Button } from "./ui/button";

export function GraphsSidebarToggle({
  className,
}: ComponentProps<typeof SidebarTrigger>) {
  const { toggleSidebar } = useSidebar();

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Button
          className={cn("h-8 px-2 md:h-fit md:px-2", className)}
          data-testid="sidebar-toggle-button"
          onClick={toggleSidebar}
          variant="outline"
        >
          <PanelLeft size={16} />
        </Button>
      </TooltipTrigger>
      <TooltipContent align="start" className="hidden md:block">
        Toggle Graphs Sidebar
      </TooltipContent>
    </Tooltip>
  );
}

export function AgentSidebarToggle({
  className,
}: ComponentProps<typeof SidebarTrigger>) {
  const { toggleRightSidebar } = useSidebar();

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Button
          className={cn("h-8 px-2 md:h-fit md:px-2", className)}
          data-testid="sidebar-toggle-button"
          onClick={toggleRightSidebar}
          variant="outline"
        >
          <PanelRight size={16} />
        </Button>
      </TooltipTrigger>
      <TooltipContent align="start" className="hidden md:block">
        Toggle Agent Sidebar
      </TooltipContent>
    </Tooltip>
  );
}

