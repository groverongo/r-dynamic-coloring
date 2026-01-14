import { Toast } from "radix-ui";
import { useRef, useState } from "react";
import { Button } from "./ui/button";

import { MainCanvasContext } from "@/lib/graph-constants";
import { useGraphCanvasContext } from "@r-dynamic-coloring/graph-canvas";
import { Image, ImageDown } from "lucide-react";
import "../styles/SaveGraphVersion.css";
import { TooltipHeaderButton } from "./ui/tooltip-header-button";


export function ImageExport({ download }: { download?: boolean }) {

  const [open, setOpen] = useState(false);
  const timerRef = useRef<NodeJS.Timeout>();

  const { saveAsImage } = useGraphCanvasContext(MainCanvasContext);

  const saveAsPNG = (e: React.MouseEvent) => {
    saveAsImage(download);

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
          {download ? <ImageDown />
            : <Image />
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