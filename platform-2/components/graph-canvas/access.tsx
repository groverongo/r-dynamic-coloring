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
    <div>
      <GraphCanvasProvider context={MainCanvasContext}>
        <GraphCanvas
          context={MainCanvasContext}
          fontSize={16}
          nodeRadius={16}
          theme={theme}
          styleProps={{
            width: 800,
            height: 800,
            borderColor: "red",
            borderWidth: "2px",
            borderStyle: "solid",
            borderRadius: "15px",
          }}
        />
      </GraphCanvasProvider>
    </div>
  );
};
