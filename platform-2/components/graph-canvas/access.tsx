"use client";

import { MainCanvasContext } from "@/lib/graph-constants";
import {
  GraphCanvas,
  GraphCanvasProvider,
} from "@r-dynamic-coloring/graph-canvas";
import { useTheme } from "next-themes";

export const AccessGraphCanvas = () => {
  const { theme } = useTheme();

  return (
    <div className="mx-auto flex items-center justify-center">
      <GraphCanvasProvider context={MainCanvasContext}>
        <GraphCanvas
          context={MainCanvasContext}
          fontSize={16}
          nodeRadius={16}
          theme={theme}
          styleProps={{
            width: 1000,
            height: 800,
            borderColor: "var(--border-color)",
            borderWidth: "2px",
            borderStyle: "solid",
            borderRadius: "15px",
          }}
        />
      </GraphCanvasProvider>
    </div>
  );
};
