"use client";

import { useEffect, useRef, useState } from "react";
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
import { useChatVisibility } from "@/hooks/use-chat-visibility";
import type { AppUsage } from "@/lib/usage";
import { generateUUID } from "@/lib/utils";
import type { VisibilityType } from "./visibility-selector";
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from "@/lib/queries";
import Canvas from "./graph-canvas";
import { ColoringParameters } from "./coloring-parameters";
import { LPSolution } from "./linear-programming-solution";
import { EngineProperties } from "./element-properties";
import { useAtomValue } from "jotai";
import { graphAdjacencyListAtom } from "@/lib/atoms";
import { ChatAgent } from "./chat-agent";

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
  const { visibilityType } = useChatVisibility({
    chatId: id ?? generateUUID(),
    initialVisibilityType,
  });


  const [input, setInput] = useState<string>("");
  const [usage, setUsage] = useState<AppUsage | undefined>(initialLastContext);
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
            <Canvas id={id} />
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
