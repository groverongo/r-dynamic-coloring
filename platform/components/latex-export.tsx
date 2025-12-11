import { Button } from "./ui/button";
import { Toast } from "radix-ui";
import { useRef, useState } from "react";

import "../styles/SaveGraphVersion.css";
import { Braces, FileJson, FilePen, PenTool } from "lucide-react";
import { edgeGraphAtom, graphAdjacencyListAtom, stylePropsAtom, vertexGraphAtom } from "@/lib/atoms";
import { useAtomValue } from "jotai";
import { TooltipHeaderButton } from "./ui/tooltip-header-button";
import { GraphTikz } from "@/lib/latex";


export function LATEXExport({download}: {download?: boolean}){

  const [open, setOpen] = useState(false);
  const timerRef = useRef<NodeJS.Timeout>();
  const vertexGraph = useAtomValue(vertexGraphAtom);
  const edgeGraph = useAtomValue(edgeGraphAtom);
  const styleProps = useAtomValue(stylePropsAtom);
  
  const saveAsLatex = (e: React.MouseEvent) => {

    const latexBuilder = new GraphTikz(vertexGraph, edgeGraph, styleProps);
    const latexCode = latexBuilder.Picture();
    console.log(latexCode)
    const blob = new Blob([latexCode], {type: 'application/txt'});
    
    if(download) {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'graph.tex';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } else {
      navigator.clipboard.writeText(latexCode);
    }

    setOpen(false);
    globalThis.clearTimeout(timerRef.current);
    timerRef.current = globalThis.setTimeout(() => {
      setOpen(true);
    }, 100);
  }

  const tooltipContent = download ? "Download JSON" : "Copy JSON to clipboard";

  return (
  <>
    <TooltipHeaderButton tooltipContent={tooltipContent}>
      <Button
        className="order-2 ml-auto h-8 px-2 md:order-1 md:ml-0 md:h-fit md:px-2"
        variant="outline"
        onClick={saveAsLatex}
      >
        {download ? <FilePen/>
        : <PenTool/>
        }
        <span className="md:sr-only">Export to json</span>
      </Button>
    </TooltipHeaderButton>
    <Toast.Provider swipeDirection="right">
      
      <Toast.Root className="ToastRoot bg-neutral-50 dark:bg-neutral-900 border border-emerald-200 dark:border-emerald-800" open={open} onOpenChange={setOpen}>
				<Toast.Title className="ToastTitle text-zinc-900 dark:text-zinc-200">{download ? "JSON downloaded" : "JSON copied to clipboard"} 😄</Toast.Title>
			</Toast.Root>
			<Toast.Viewport className="ToastViewport" />
    </Toast.Provider>
  </>
  )
}