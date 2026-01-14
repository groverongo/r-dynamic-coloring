
import { EdgeRef } from "../Edge/ref";
import { VertexRef } from "../Vertex/ref";

export type vertexRefsType = Map<string, VertexRef | null>;

export type edgeRefsType = Map<string, EdgeRef | null>;

export type graphAdjacencyListType = Map<string, Set<[string, string]>>;

export type vertexGraphType = Map<string, { x: number, y: number, xRelative: number, yRelative: number }>;

export type edgeGraphType = Map<string, { from: string, to: string, fromEntry: [string, string], toEntry: [string, string] }>;

export type coloringType = Record<string, number>;