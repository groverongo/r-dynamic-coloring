import Konva from "konva";
import { Context, Dispatch, ReactNode, RefObject, SetStateAction, useRef, useState } from "react";

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
