"use client";

import { MainCanvasContext } from "@/lib/graph-constants";
import { queryClient } from "@/lib/queries";
import { GraphCanvasProvider } from "@r-dynamic-coloring/graph-canvas";
import { QueryClientProvider } from "@tanstack/react-query";
import { ReactNode } from "react";

export function Providers({ children }: { children: ReactNode }) {
    return (
        <QueryClientProvider client={queryClient}>
            <GraphCanvasProvider context={MainCanvasContext}>
                {children}
            </GraphCanvasProvider>
        </QueryClientProvider>
    );
}
