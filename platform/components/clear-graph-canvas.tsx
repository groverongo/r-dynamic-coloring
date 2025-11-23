import { Button } from "./ui/button";
import { Dialog, Toast } from "radix-ui";
import { MouseEventHandler, useRef, useState } from "react";

import { useSetAtom } from "jotai";
import { coloringAtom, edgeGraphAtom, graphAdjacencyListAtom, vertexGraphAtom, vertexCurrentIdAtom, edgeCurrentIdAtom } from "@/lib/atoms";
import { TooltipHeaderButton } from "./ui/tooltip-header-button";
import { Eraser } from "lucide-react";
import { useElementRef } from "@/lib/refs";

import "../styles/SaveGraphVersion.css";
import "../styles/ClearGraphDialog.css";

export function ClearGraphCanvas(){

  const [openToast, setOpenToast] = useState(false);
  const [openDialog, setOpenDialog] = useState(false);
  const timerRef = useRef<NodeJS.Timeout>();

  const setVertexGraph = useSetAtom(vertexGraphAtom);
  const setEdgeGraph = useSetAtom(edgeGraphAtom);
  const setGraphStructure = useSetAtom(graphAdjacencyListAtom);
  const setVertexCurrentId = useSetAtom(vertexCurrentIdAtom);
  const setEdgeCurrentId = useSetAtom(edgeCurrentIdAtom);
  const setColoring = useSetAtom(coloringAtom);

  const { vertexRefs, edgeRefs } = useElementRef();

  const clearCanvas = () => {
    setVertexGraph(new Map<string, {x: number, y: number, xRelative: number, yRelative: number}>());
    setEdgeGraph(new Map<string, {from: string, to: string, fromEntry: [string, string], toEntry: [string, string]}>());
    setGraphStructure(new Map<string, Set<[string, string]>>());
    setVertexCurrentId(null);
    setEdgeCurrentId(null);
    setColoring({});
    vertexRefs.current?.clear();
    edgeRefs.current?.clear();
    
    setOpenToast(false);
    globalThis.clearTimeout(timerRef.current);
    timerRef.current = globalThis.setTimeout(() => {
      setOpenToast(true);
    }, 100);
  }

  const clearCanvasConfirm: MouseEventHandler<HTMLButtonElement> = (e) => {
    clearCanvas();
  };

  return (
  <>
    <Dialog.Root open={openDialog} onOpenChange={setOpenDialog}>
      <Dialog.Trigger asChild>
        <TooltipHeaderButton tooltipContent="Clear graph canvas">
          <Button
            className="order-2 ml-auto h-8 px-2 md:order-1 md:ml-0 md:h-fit md:px-2"
            variant="outline"
            onClick={() => setOpenDialog(true)}
          >
            <Eraser/>
            <span className="md:sr-only">Clear graph</span>
          </Button>
        </TooltipHeaderButton>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="DialogOverlay" />
        <Dialog.Content className="DialogContent">
          <Dialog.Title className="DialogTitle"><span className="text-2xl">Clear</span></Dialog.Title>
          <Dialog.Description className="DialogDescription text-zinc-900 dark:text-zinc-200">
            <span className="text-sm">Are you sure you want to clear the canvas?</span>
          </Dialog.Description>
          <Dialog.Close asChild>
            <Button
              className="hover:bg-zinc-50 dark:hover:bg-zinc-800 bg-zinc-50 dark:bg-zinc-900 border border-emerald-200 dark:border-emerald-800"
              variant="outline"
              style={{ marginRight: "1rem" }}
              onClick={clearCanvasConfirm}
            >
              Yes
            </Button>
          </Dialog.Close>
          <Dialog.Close asChild>
            <Button
              className="hover:bg-zinc-50 dark:hover:bg-zinc-800 bg-zinc-50 dark:bg-zinc-900 border border-rose-200 dark:border-rose-800"
              variant="outline"
              style={{ marginRight: "1rem" }}
            >
              No
            </Button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
      
    <Toast.Provider swipeDirection="right">
      <Toast.Root className="ToastRoot bg-zinc-50 dark:bg-zinc-900 border border-emerald-200 dark:border-emerald-800" open={openToast} onOpenChange={setOpenToast}>
				<Toast.Title className="ToastTitle text-zinc-900 dark:text-zinc-200">Graph was cleared 😄</Toast.Title>
			</Toast.Root>
			<Toast.Viewport className="ToastViewport" />
    </Toast.Provider>
  </>
  )
}