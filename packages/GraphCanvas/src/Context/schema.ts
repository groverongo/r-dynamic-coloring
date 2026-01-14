import Konva from "konva";
import { Dispatch, RefObject, SetStateAction } from "react";
import { coloringType, edgeGraphType, edgeRefsType, graphAdjacencyListType, vertexGraphType, vertexRefsType } from "./state";

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

    saveAsImage: (download?: boolean) => void,
}
