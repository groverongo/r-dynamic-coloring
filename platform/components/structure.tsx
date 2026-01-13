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
import { useAtom, useSetAtom } from "jotai";
import { graphNameAtom, stylePropsAtom } from "@/lib/atoms";
import { ChatAgent } from "./chat-agent";
import { GetGraphResponse } from "@/lib/validation";
import axios from "axios";
import { GraphDeserializer } from "@/lib/serializers";
import { MainCanvasContext } from "@/lib/graph-constants";
import { GraphCanvasProvider, useGraphCanvasContext } from "./graphCanvas/useContext";
import { GraphVisualize } from "./graph-visualize";

export function Structure({
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

  const [currentModelId, setCurrentModelId] = useState(initialChatModel);
  const currentModelIdRef = useRef(currentModelId);

  const [showCreditCardAlert, setShowCreditCardAlert] = useState(false);

  useEffect(() => {
    currentModelIdRef.current = currentModelId;
  }, [currentModelId]);



  return (
    <QueryClientProvider client={queryClient}>
      <GraphCanvasProvider context={MainCanvasContext}>
        <GraphVisualize
          id={id}
          isReadonly={isReadonly}
          initialVisibilityType={initialVisibilityType}
          autoResume={autoResume}
          initialLastContext={initialLastContext}
          initialChatModel={initialChatModel}
        />
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
      </GraphCanvasProvider>
    </QueryClientProvider>
  );
}
