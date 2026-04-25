import { CSSProperties, Context } from "react";
import { ContextInterface } from "../Context/schema";

const DefaultTailwindClasses = "bg-zinc-100 dark:bg-zinc-900";

type GraphCanvasTriggers = Partial<{
  existingEdge: (vertex1: string, vertex2: string) => void;
}>

type GraphCanvasProps = {
  styleProps: CSSProperties;
  className: string;
  context: Context<ContextInterface | undefined>;
  fontSize: number;
  nodeRadius: number;
  theme: string | undefined;
  triggers?: GraphCanvasTriggers;
}

export { DefaultTailwindClasses, GraphCanvasProps };

