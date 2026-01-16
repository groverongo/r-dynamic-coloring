"use client";

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
import { MainCanvasContext } from "@/lib/graph-constants";
import { queryClient } from "@/lib/queries";
import { GraphCanvasProvider } from "@r-dynamic-coloring/graph-canvas";
import { QueryClientProvider } from '@tanstack/react-query';
import { useEffect, useRef, useState } from "react";
import { GraphVisualize } from "./graph-visualize";
import type { VisibilityType } from "./visibility-selector";

export function Structure({
  id,
  initialChatModel,
  initialVisibilityType,
  isReadonly,
}: {
  id?: string;
  initialChatModel: string;
  initialVisibilityType: VisibilityType;
  isReadonly: boolean;
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
