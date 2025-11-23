import { Save } from "lucide-react";
import { Button } from "./ui/button";
import { Toast, Tooltip } from "radix-ui";
import { useEffect, useRef, useState } from "react";

import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { useAtomValue } from "jotai";
import { graphNameAtom, coloringAtom, edgeGraphAtom, graphAdjacencyListAtom, kColorsAtom, rFactorAtom, vertexGraphAtom } from "@/lib/atoms";
import {GraphSerializer} from "@/lib/serializers";
import "../styles/SaveGraphVersion.css";
import { TooltipHeaderButton } from "./ui/tooltip-header-button";

const ToastConditionComponents = {
  success: {
    title: <Toast.Title className="ToastTitle text-zinc-900 dark:text-zinc-200">Graph saved has been saved 😄</Toast.Title>,
    description: (savedGraphId: string) => <Toast.Description className="ToastDescription">with id: {savedGraphId}</Toast.Description>,
  },
  failure: {
    title: <Toast.Title className="ToastTitle text-zinc-900 dark:text-zinc-200">Graph saved was not saved 😭</Toast.Title>,
    description: (errorMessage: string) => <Toast.Description className="ToastDescription">{errorMessage}</Toast.Description>,
  }
}

interface CreateGraphRequest {
  name: string;
  graphAdjacencyList: string;
  vertexGraph: string;
  edgeGraph: string;
  localColoring: string;
  localK: number;
  localR: number;
}

interface CreateGraphResponse {
  id: string;
}

export function SaveGraphVersion(){

  const [open, setOpen] = useState(false);
  const timerRef = useRef<NodeJS.Timeout>();
  const [savedGraphId, setSavedGraphId] = useState<string>("");

  const graphName = useAtomValue(graphNameAtom);
  const vertexGraph = useAtomValue(vertexGraphAtom);
  const edgeGraph = useAtomValue(edgeGraphAtom);
  const graphAdjacencyList = useAtomValue(graphAdjacencyListAtom);
  const coloring = useAtomValue(coloringAtom);
  const kColors = useAtomValue(kColorsAtom);
  const rFactor = useAtomValue(rFactorAtom);

  const { isSuccess, error, mutate, data } = useMutation({
    mutationFn: async () => {
      const request: CreateGraphRequest = {
        name: graphName,
        graphAdjacencyList: GraphSerializer.graphAdjacencyListSerializer(graphAdjacencyList),
        vertexGraph: GraphSerializer.vertexGraphSerializer(vertexGraph),
        edgeGraph: GraphSerializer.edgeGraphSerializer(edgeGraph),
        localColoring: GraphSerializer.coloringSerializer(coloring),
        localK: kColors,
        localR: rFactor,
      }
      const response = await axios.post(`${process.env.NEXT_PUBLIC_R_HUED_COLORING_API}/graphs`, request);
      return response.data as CreateGraphResponse;
    },
    retry: false,
  });

  useEffect(() => {
    if(isSuccess) {
      setSavedGraphId(data?.id ?? "");
    }
  }, [isSuccess, data]);

  const saveGraphVersion = () => {
    mutate();

    setOpen(false);
    globalThis.clearTimeout(timerRef.current);
    timerRef.current = globalThis.setTimeout(() => {
      setOpen(true);
    }, 100);
  }

  return (
  <>
    <TooltipHeaderButton tooltipContent="Save graph version">
      <Button
        className="order-2 ml-auto h-8 px-2 md:order-1 md:ml-0 md:h-fit md:px-2"
        variant="outline"
        onClick={saveGraphVersion}
      >
        <Save/>
        <span className="md:sr-only">Save Graph Version</span>
      </Button>
    </TooltipHeaderButton>
      
    <Toast.Provider swipeDirection="right">
      <Toast.Root className="ToastRoot bg-neutral-50 dark:bg-neutral-900 border border-emerald-200 dark:border-emerald-800" open={open} onOpenChange={setOpen}>
				{ToastConditionComponents[isSuccess ? "success" : "failure"].title}
				{ToastConditionComponents[isSuccess ? "success" : "failure"].description(isSuccess ? savedGraphId : JSON.stringify(error))}
			</Toast.Root>
			<Toast.Viewport className="ToastViewport" />
    </Toast.Provider>
  </>
  )
}