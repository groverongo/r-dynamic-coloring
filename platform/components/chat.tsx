"use client";

import { CSSProperties, useEffect, useRef, useState } from "react";
import { ChatHeader } from "@/components/chat-header";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import type { AppUsage } from "@/lib/usage";
import type { VisibilityType } from "./visibility-selector";
import { QueryClientProvider, useQuery } from '@tanstack/react-query';
import { queryClient } from "@/lib/queries";
import Canvas from "./graph-canvas";
import { ColoringParameters } from "./coloring-parameters";
import { LPSolution } from "./linear-programming-solution";
import { EngineProperties } from "./element-properties";
import { useAtom, useAtomValue, useSetAtom } from "jotai";
import { coloringAtom, edgeGraphAtom, graphAdjacencyListAtom, graphNameAtom, kColorsAtom, rFactorAtom, stylePropsAtom, vertexGraphAtom } from "@/lib/atoms";
import { ChatAgent } from "./chat-agent";
import { GetGraphResponse } from "@/lib/validation";
import axios from "axios";
import { GraphDeserializer } from "@/lib/serializers";

export function GraphVisualize({
  id,
  initialChatModel,
  initialVisibilityType,
  isReadonly,
  autoResume,
  initialLastContext,
}: {
  id?: string;
  initialChatModel: string;
  initialVisibilityType: VisibilityType;
  isReadonly: boolean;
  autoResume: boolean;
  initialLastContext?: AppUsage;
}) {
  const [styleProps, setStyleProps] = useAtom<CSSProperties>(stylePropsAtom);

  const setGraphName = useSetAtom(graphNameAtom);
  const setVertexGraph = useSetAtom(vertexGraphAtom);
  const setEdgeGraph = useSetAtom(edgeGraphAtom);
  const setGraphAdjacencyList = useSetAtom(graphAdjacencyListAtom);
  const setKColors = useSetAtom(kColorsAtom);
  const setRFactor = useSetAtom(rFactorAtom);
  const setColoring = useSetAtom(coloringAtom);

  useEffect(() => {
    console.log(screen.width, screen.height)
    setStyleProps({
      height: screen.height / 1.6,
      width: (1200 * screen.width) / 2000,
      border: "3px solid white",
      borderRadius: "15px",
    });
  }, []);

  const { refetch, data } = useQuery({
    queryKey: ["graph", id],
    queryFn: async () => {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_R_HUED_COLORING_API}/graphs/${id}`)
      return response.data as GetGraphResponse;
    },
    retryOnMount: false,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    refetchOnReconnect: false,
  });

  useEffect(() => {
    if (!id) return;
    refetch().then((response) => {
      if (response.data === undefined) return;

      setGraphName(response.data.name);
      setGraphAdjacencyList(GraphDeserializer.graphAdjacencyListDeserializer(response.data.graphAdjacencyList));
      setVertexGraph(GraphDeserializer.vertexGraphDeserializer(response.data.vertexGraph));
      setEdgeGraph(GraphDeserializer.edgeGraphDeserializer(response.data.edgeGraph));
      setColoring(GraphDeserializer.coloringDeserializer(response.data.localColoring));
      setKColors(response.data.localK);
      setRFactor(response.data.localR);
    });
  }, []);

  const [showCreditCardAlert, setShowCreditCardAlert] = useState(false);
  const [currentModelId, setCurrentModelId] = useState(initialChatModel);
  const currentModelIdRef = useRef(currentModelId);

  const graphAdjacencyList = useAtomValue(graphAdjacencyListAtom);

  useEffect(() => {
    currentModelIdRef.current = currentModelId;
  }, [currentModelId]);



  return (
    <QueryClientProvider client={queryClient}>
      <div className="overscroll-behavior-contain flex h-dvh min-w-0 touch-pan-y flex-col bg-background">
        <ChatHeader
          chatId={id}
          isReadonly={isReadonly}
          selectedVisibilityType={initialVisibilityType}
        />

        <div className="flex flex-row items-stretch gap-1 sm:gap-2 flex-1 overflow-hidden">
          <div className="flex-1 flex flex-col items-center justify-center gap-1 sm:gap-2 overflow-y-auto p-4">
            <Canvas key={id} styleProps={styleProps} />
            <div className="flex flex-row gap-1 sm:gap-2">
              <ColoringParameters />
              <LPSolution />
              <EngineProperties />
            </div>
          </div>

          <div className="flex flex-col w-full max-w-2xl border-l-2 border-border overflow-hidden">
            <ChatAgent />
          </div>
        </div>
      </div>

      <AlertDialog
        onOpenChange={setShowCreditCardAlert}
        open={showCreditCardAlert}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Activate AI Gateway</AlertDialogTitle>
            <AlertDialogDescription>
              This application requires{" "}
              {process.env.NODE_ENV === "production" ? "the owner" : "you"} to
              activate Vercel AI Gateway.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={() => {
                window.open(
                  "https://vercel.com/d?to=%2F%5Bteam%5D%2F%7E%2Fai%3Fmodal%3Dadd-credit-card",
                  "_blank"
                );
                window.location.href = "/";
              }}
            >
              Activate
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </QueryClientProvider>
  );
}
