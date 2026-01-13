import { Ref } from "react";
import VertexRef from "./ref";

type VertexProps = {
  ref?: Ref<VertexRef>;
  colorIndexInitial: number | null;
  x: number;
  y: number;
  onSelect?: () => void;
  draggable?: boolean;
  mode: number;
  compromised?: boolean;
  whileDragging?: (x: number, y: number) => void;
  allowedColors?: Set<number>;
  theme: 'light' | 'dark';
  fontSize: number;
  nodeRadius: number;
};

export default VertexProps;
