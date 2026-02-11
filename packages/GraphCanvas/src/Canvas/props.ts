import { CSSProperties, Context } from "react";
import { ContextInterface } from "../Context/schema";

type GraphCanvasTriggers = Partial<{
  existingEdge: (vertex1: string, vertex2: string) => void;
}>

type GraphCanvasProps = {
  styleProps: CSSProperties;
  context: Context<ContextInterface | undefined>;
  fontSize: number;
  nodeRadius: number;
  theme: string | undefined;
  triggers?: GraphCanvasTriggers;
}

export { GraphCanvasProps };
