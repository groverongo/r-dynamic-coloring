'use client'

import Konva from "konva";
import { Context, ReactNode, createContext, useContext, useRef, useState } from "react";
import EdgeRef from "../Edge/ref";
import VertexRef from "../Vertex/ref";
import { ContextInterface } from "./schema";
import { coloringType, edgeGraphType, edgeRefsType, graphAdjacencyListType, vertexGraphType, vertexRefsType } from "./state";


export const useGraphCanvasContext = (context: Context<ContextInterface | undefined>) => {
    const contextValue = useContext(context);
    if (contextValue === undefined) {
        throw new Error("useGraphCanvasContext must be used within a GraphCanvasProvider");
    }
    return contextValue;
};

export function createGraphCanvasContext() {
    return createContext<ContextInterface | undefined>(undefined);
}


export const GraphCanvasProvider: React.FC<{
    context: Context<ContextInterface | undefined>;
    children?: ReactNode;
}> = ({ context, children }) => {
    const stageRef = useRef<Konva.Stage | null>(null);
    const vertexRefs = useRef<vertexRefsType>(new Map<string, VertexRef | null>());
    const edgeRefs = useRef<edgeRefsType>(new Map<string, EdgeRef | null>());

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