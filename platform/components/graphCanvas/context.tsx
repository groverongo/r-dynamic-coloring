import Konva from "konva";
import { Context, Dispatch, ReactNode, RefObject, SetStateAction, createContext, useContext, useRef, useState } from "react";

import { NodeGRef } from "../graphObjects/node";
import { LinkGRef } from "../graphObjects/link";

export type vertexRefsType = Map<string, NodeGRef | null>;
export type edgeRefsType = Map<string, LinkGRef | null>;

export type graphAdjacencyListType = Map<string, Set<[string, string]>>;
export type vertexGraphType = Map<string, { x: number, y: number, xRelative: number, yRelative: number }>;
export type edgeGraphType = Map<string, { from: string, to: string, fromEntry: [string, string], toEntry: [string, string] }>;
export type coloringType = Record<string, number>;

export interface ContextInterface {
    rFactor: number;
    setRFactor: Dispatch<SetStateAction<number>>;

    kColors: number;
    setKColors: Dispatch<SetStateAction<number>>;

    vertexGraph: vertexGraphType;
    setVertexGraph: Dispatch<SetStateAction<vertexGraphType>>;

    edgeGraph: edgeGraphType;
    setEdgeGraph: Dispatch<SetStateAction<edgeGraphType>>;

    graphAdjacencyList: graphAdjacencyListType;
    setGraphAdjacencyList: Dispatch<SetStateAction<graphAdjacencyListType>>;

    coloring: coloringType;
    setColoring: Dispatch<SetStateAction<coloringType>>;

    vertexCurrentId: string | null;
    setVertexCurrentId: Dispatch<SetStateAction<string | null>>;

    edgeCurrentId: string | null;
    setEdgeCurrentId: Dispatch<SetStateAction<string | null>>;

    stageRef: RefObject<Konva.Stage | null>,
    vertexRefs: RefObject<vertexRefsType>,
    edgeRefs: RefObject<edgeRefsType>,

    clearCanvas: () => void,
}

export function createGraphCanvasContext() {
    return createContext<ContextInterface | undefined>(undefined);
}

export const useGraphCanvasContext = (context: Context<ContextInterface | undefined>) => {
    const contextValue = useContext(context);
    if (contextValue === undefined) {
        throw new Error("useGraphCanvasContext must be used within a GraphCanvasProvider");
    }
    return contextValue;
};

export const GraphCanvasProvider: React.FC<{
    context: Context<ContextInterface | undefined>;
    children?: ReactNode;
}> = ({ context, children }) => {
    const stageRef = useRef<Konva.Stage | null>(null);
    const vertexRefs = useRef<vertexRefsType>(new Map<string, NodeGRef | null>());
    const edgeRefs = useRef<edgeRefsType>(new Map<string, LinkGRef | null>());

    const [rFactor, setRFactor] = useState<number>(1);
    const [kColors, setKColors] = useState<number>(1);
    const [vertexCurrentId, setVertexCurrentId] = useState<string | null>(null);
    const [edgeCurrentId, setEdgeCurrentId] = useState<string | null>(null);

    const [vertexGraph, setVertexGraph] = useState<vertexGraphType>(new Map<string, { x: number, y: number, xRelative: number, yRelative: number }>());
    const [edgeGraph, setEdgeGraph] = useState<edgeGraphType>(new Map<string, { from: string, to: string, fromEntry: [string, string], toEntry: [string, string] }>());
    const [graphAdjacencyList, setGraphAdjacencyList] = useState<graphAdjacencyListType>(new Map<string, Set<[string, string]>>());
    const [coloring, setColoring] = useState<coloringType>({});

    function clearCanvas() {
        setVertexGraph(new Map<string, { x: number, y: number, xRelative: number, yRelative: number }>());
        setEdgeGraph(new Map<string, { from: string, to: string, fromEntry: [string, string], toEntry: [string, string] }>());
        setGraphAdjacencyList(new Map<string, Set<[string, string]>>());
        setColoring({});
        vertexRefs.current?.clear();
        edgeRefs.current?.clear();
    }

    return (
        <context.Provider value={{
            rFactor, setRFactor,
            kColors, setKColors,
            vertexGraph, setVertexGraph,
            edgeGraph, setEdgeGraph,
            graphAdjacencyList, setGraphAdjacencyList,
            coloring, setColoring,
            vertexCurrentId, setVertexCurrentId,
            edgeCurrentId, setEdgeCurrentId,
            stageRef, vertexRefs, edgeRefs,
            clearCanvas
        }}>
            {children}
        </context.Provider>
    );
};