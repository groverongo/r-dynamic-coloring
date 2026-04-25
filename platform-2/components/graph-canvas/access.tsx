"use client";

import { MainCanvasContext } from "@/lib/graph-constants";
import { cn } from "@/lib/utils";
import {
  DefaultTailwindClasses,
  GraphCanvas,
  GraphCanvasProvider
} from "@r-dynamic-coloring/graph-canvas";
import { useTheme } from "next-themes";

export const AccessGraphCanvas = () => {
  const { theme } = useTheme();



  return (
    <div className="mx-auto h-full w-19/20 flex items-center justify-center">
      <GraphCanvasProvider context={MainCanvasContext}>
        <GraphCanvas
          context={MainCanvasContext}
          fontSize={16}
          nodeRadius={16}
          theme={theme}
          styleProps={{
            height: 1000
          }}
          className={cn(DefaultTailwindClasses, "border-2 border-zinc-700 dark:border-zinc-200 rounded-xl")}
        />
      </GraphCanvasProvider>
    </div>
  );
};
