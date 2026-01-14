"use client";

import { ChatHeader } from "@/components/chat-header";
import { fontSizeAtom, graphNameAtom, nodeRadiusAtom, stylePropsAtom } from "@/lib/atoms";
import { MainCanvasContext } from "@/lib/graph-constants";
import { GraphDeserializer } from "@/lib/serializers";
import type { AppUsage } from "@/lib/usage";
import { GetGraphResponse } from "@/lib/validation";
import { useQuery } from '@tanstack/react-query';
import axios from "axios";
import { useAtom, useAtomValue, useSetAtom } from "jotai";
import { useTheme } from "next-themes";
import { CSSProperties, useEffect, useRef, useState } from "react";
import GraphCanvas from "./GraphCanvas/Canvas/graph-canvas";
import { useGraphCanvasContext } from "./GraphCanvas/Context/useContext";
import { ChatAgent } from "./chat-agent";
import { ColoringParameters } from "./coloring-parameters";
import { EngineProperties } from "./element-properties";
import { LPSolution } from "./linear-programming-solution";
import type { VisibilityType } from "./visibility-selector";

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
  const { theme } = useTheme();

  const {
    setVertexGraph,
    setEdgeGraph,
    graphAdjacencyList, setGraphAdjacencyList,
    setColoring,
    rFactor, setRFactor,
    kColors, setKColors,
  } = useGraphCanvasContext(MainCanvasContext);


  const setGraphName = useSetAtom(graphNameAtom);
  const fontSize = useAtomValue(fontSizeAtom);
  const nodeRadius = useAtomValue(nodeRadiusAtom);

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


  useEffect(() => {
    currentModelIdRef.current = currentModelId;
  }, [currentModelId]);



  return (
    <>
      <div className="overscroll-behavior-contain flex h-dvh min-w-0 touch-pan-y flex-col bg-background">
        <ChatHeader
          chatId={id}
          isReadonly={isReadonly}
          selectedVisibilityType={initialVisibilityType}
        />

        <div className="flex flex-row items-stretch gap-1 sm:gap-2 flex-1 overflow-hidden">
          <div className="flex-1 flex flex-col items-center justify-center gap-1 sm:gap-2 overflow-y-auto p-4">
            <GraphCanvas
              key={id}
              styleProps={styleProps}
              context={MainCanvasContext}
              fontSize={fontSize}
              nodeRadius={nodeRadius}
              theme={theme}
            />
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
    </>
  );
}
