import { Ref } from "react";
import EdgeRef from "./ref";

type EdgeProps = {
    fromId: string;
    toId: string;
    from: { x: number, y: number };
    to: { x: number, y: number };
    ref?: Ref<EdgeRef>;
    onSelect?: () => void;
    compromised?: boolean;
    theme: 'light' | 'dark';
}

export default EdgeProps;