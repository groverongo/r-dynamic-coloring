import { Button } from "./ui/button";
import { Toast } from "radix-ui";
import { useRef, useState } from "react";

import "../styles/SaveGraphVersion.css";
import { useElementRef } from "@/lib/refs";
import { Image, ImageDown } from "lucide-react";
import Konva from "konva";
import { TooltipHeaderButton } from "./ui/tooltip-header-button";


export function ImageExport({download}: {download?: boolean}){

  const [open, setOpen] = useState(false);
  const timerRef = useRef<NodeJS.Timeout>();
  const [savedGraphId, setSavedGraphId] = useState<string>("");

  const {stageRef, vertexRefs, edgeRefs} = useElementRef();
  
  const saveAsPNG = (e: React.MouseEvent) => {
    if(stageRef.current === null) return;

    const stageClone = stageRef.current.clone();

    stageClone.getLayers()[0].add(new Konva.Rect({
      width: stageRef.current.width(),
      height: stageRef.current.height(),
      fill: '#18181b', 
      listening: false
    }));

    stageClone.toBlob({mimeType: 'image/png'}).then(blob => {
      if(download) {
        const url = URL.createObjectURL(blob as Blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'graph.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      } else {
        navigator.clipboard.write([new ClipboardItem({'image/png': blob as Blob})])
      }
    })

    setOpen(false);
    globalThis.clearTimeout(timerRef.current);
    timerRef.current = globalThis.setTimeout(() => {
      setOpen(true);
    }, 100);
  }

  const tooltipContent = download ? "Download PNG" : "Copy PNG to clipboard";

  return (
    <>
    <TooltipHeaderButton tooltipContent={tooltipContent}>
      <Button
        className="order-2 ml-auto h-8 px-2 md:order-1 md:ml-0 md:h-fit md:px-2"
        variant="outline"
        onClick={saveAsPNG}
      >
        {download ? <ImageDown/>
        : <Image/>
        }
        <span className="md:sr-only">{tooltipContent}</span>
      </Button>
    </TooltipHeaderButton>

    <Toast.Provider swipeDirection="right">
      <Toast.Root className="ToastRoot bg-neutral-50 dark:bg-neutral-900 border border-emerald-200 dark:border-emerald-800" open={open} onOpenChange={setOpen}>
				<Toast.Title className="ToastTitle text-zinc-900 dark:text-zinc-200">{download ? "PNG downloaded" : "PNG copied to clipboard"} 😄</Toast.Title>
			</Toast.Root>
			<Toast.Viewport className="ToastViewport" />
    </Toast.Provider>
    </>
  )
}