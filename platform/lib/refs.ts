import { LinkGRef } from "@/components/graphObjects/link";
import { NodeGRef } from "@/components/graphObjects/node";
import Konva from "konva";
import { createContext, RefObject, useContext } from "react";

export type vertexRefsType = Map<string, NodeGRef | null>;
export type edgeRefsType = Map<string, LinkGRef | null>;

export const ElementRefContext = createContext<{
    stageRef: RefObject<Konva.Stage | null>,
    vertexRefs: RefObject<vertexRefsType>,
    edgeRefs: RefObject<edgeRefsType>,
}>({
    stageRef: { current: null },
    vertexRefs: { current: new Map<string, NodeGRef | null>() },
    edgeRefs: { current: new Map<string, LinkGRef | null>() },
});

export const useElementRef = () => useContext(ElementRefContext);

export const OperationFlagsRefContext = createContext<{
    shiftRef: RefObject<boolean>,
    inCanvasRef: RefObject<boolean>,
    caretVisibleRef: RefObject<boolean>
}>({
    shiftRef: { current: false },
    inCanvasRef: { current: false },
    caretVisibleRef: { current: true }
});

export const useOperationFlagsRef = () => useContext(OperationFlagsRefContext);