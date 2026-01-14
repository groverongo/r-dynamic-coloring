import { CSSProperties, Context } from "react";
import { ContextInterface } from "../Context/schema";

type GraphCanvasProps = {
  styleProps: CSSProperties;
  context: Context<ContextInterface | undefined>;
  fontSize: number;
  nodeRadius: number;
  theme: string | undefined;
}

export default GraphCanvasProps;