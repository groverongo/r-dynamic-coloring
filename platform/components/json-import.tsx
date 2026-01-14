import { Toast } from "radix-ui";
import { useRef, useState } from "react";
import { Button } from "./ui/button";

import { stylePropsAtom } from "@/lib/atoms";
import { MainCanvasContext } from "@/lib/graph-constants";
import { ImportGraphInput, ImportGraphInputSchema } from "@/lib/validation";
import { edgeGraphType, graphAdjacencyListType, useGraphCanvasContext, vertexGraphType } from "@r-dynamic-coloring/graph-canvas";
import { useAtomValue } from "jotai";
import { Braces, FileJson } from "lucide-react";
import { v4 as uuidv4 } from 'uuid';
import "../styles/SaveGraphVersion.css";
import { TooltipHeaderButton } from "./ui/tooltip-header-button";


export function JSONImport({ upload }: { upload?: boolean }) {

  const [open, setOpen] = useState(false);
  const timerRef = useRef<NodeJS.Timeout>();

  // atoms to be updated
  const {
    setColoring,
    setKColors,
    setGraphAdjacencyList,
    setVertexGraph,
    setEdgeGraph
  } = useGraphCanvasContext(MainCanvasContext);

  // atoms to be read
  const styleProps = useAtomValue(stylePropsAtom);

  // utility functions
  const getMaxColors = ({ coloring }: ImportGraphInput) => Math.max(...Object.values(coloring));
  const createVertexAtom = ({ graph, vertexPositions }: ImportGraphInput): vertexGraphType => {

    const { width, height } = styleProps;

    let vertexData: vertexGraphType = new Map();
    for (const vertexId of Object.keys(graph)) {
      const vertexPosition = vertexPositions[vertexId] ?? [0, 0];
      vertexData.set(vertexId, {
        x: vertexPosition[0],
        y: vertexPosition[1],
        xRelative: vertexPosition[0],
        yRelative: vertexPosition[1]
      });
    }
    return vertexData;
  }
  const createEdgeAtom = ({ graph }: ImportGraphInput): edgeGraphType => {
    let edgeData: edgeGraphType = new Map();
    let checkedVertices: Record<string, Record<string, boolean>> = {};

    for (const fromVertexId of Object.keys(graph)) {
      checkedVertices[fromVertexId] = {};
    }

    for (const fromVertexId of Object.keys(graph)) {
      for (const toVertexId of graph[fromVertexId]) {
        if (checkedVertices[fromVertexId][toVertexId]) continue;

        checkedVertices[fromVertexId][toVertexId] = true;
        checkedVertices[toVertexId][fromVertexId] = true;

        const edgeId = uuidv4();
        edgeData.set(edgeId, {
          from: fromVertexId,
          to: toVertexId,
          fromEntry: [fromVertexId, edgeId],
          toEntry: [toVertexId, edgeId]
        });
      }
    }
    return edgeData;
  }
  const createAdjacencyListAtom = (vertexGraph: vertexGraphType, edges: edgeGraphType): graphAdjacencyListType => {
    let adjacencyList: graphAdjacencyListType = new Map();

    for (const fromVertexId of vertexGraph.keys()) {
      adjacencyList.set(fromVertexId, new Set());
    }

    for (const [edgeId, edge] of edges.entries()) {
      adjacencyList.get(edge.from)?.add([edge.to, edgeId]);
      adjacencyList.get(edge.to)?.add([edge.from, edgeId]);
    }

    return adjacencyList;
  }


  // update atoms
  const updateAtoms = (parsedJson: ImportGraphInput) => {
    const vertexGraph = createVertexAtom(parsedJson);
    const edgeGraph = createEdgeAtom(parsedJson);
    const adjacencyList = createAdjacencyListAtom(vertexGraph, edgeGraph);
    const k = getMaxColors(parsedJson);
    const coloring = parsedJson.coloring;

    setGraphAdjacencyList(adjacencyList);
    setVertexGraph(vertexGraph);
    setEdgeGraph(edgeGraph);
    setKColors(k);
    setColoring(coloring);
  }


  const importJSON = async (e: React.MouseEvent) => {

    let parsedJson: ImportGraphInput;

    if (upload) {

    } else {
      const importText = await navigator.clipboard.readText();
      const rawJson = JSON.parse(importText);
      parsedJson = ImportGraphInputSchema.parse(rawJson);

      updateAtoms(parsedJson);
    }

    setOpen(false);
    globalThis.clearTimeout(timerRef.current);
    timerRef.current = globalThis.setTimeout(() => {
      setOpen(true);
    }, 100);
  }

  const tooltipContent = upload ? "Import graph from JSON file" : "Import graph from JSON clipboard";

  return (
    <>
      <TooltipHeaderButton tooltipContent={tooltipContent}>
        <Button
          className="order-2 ml-auto h-8 px-2 md:order-1 md:ml-0 md:h-fit md:px-2"
          variant="outline"
          onClick={importJSON}
        >
          {upload ? <FileJson />
            : <Braces />
          }
          <span className="md:sr-only">Import graph from JSON</span>
        </Button>
      </TooltipHeaderButton>
      <Toast.Provider swipeDirection="right">

        <Toast.Root className="ToastRoot bg-neutral-50 dark:bg-neutral-900 border border-emerald-200 dark:border-emerald-800" open={open} onOpenChange={setOpen}>
          <Toast.Title className="ToastTitle text-zinc-900 dark:text-zinc-200">{upload ? "JSON uploaded" : "JSON copied to clipboard"} 😄</Toast.Title>
        </Toast.Root>
        <Toast.Viewport className="ToastViewport" />
      </Toast.Provider>
    </>
  )
}