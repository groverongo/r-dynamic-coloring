"use client";

import { MainCanvasContext } from "@/lib/graph-constants";
import { queryClient } from "@/lib/queries";
import { GraphCanvasProvider } from "@r-dynamic-coloring/graph-canvas";
import { QueryClientProvider } from "@tanstack/react-query";
import { AgentChat } from "./AgentChat";

export function ChatAgentSidebar() {

  return (
    <QueryClientProvider client={queryClient}>
      <GraphCanvasProvider context={MainCanvasContext}>

        <AgentChat.AgentChatSidebar />

      </GraphCanvasProvider>
    </QueryClientProvider>
  );
}
