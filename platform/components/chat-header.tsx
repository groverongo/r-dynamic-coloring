"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { memo } from "react";
import { useWindowSize } from "usehooks-ts";
import { SidebarToggle } from "@/components/sidebar-toggle";
import { Button } from "@/components/ui/button";
import { PlusIcon, VercelIcon } from "./icons";
import { useSidebar } from "./ui/sidebar";
import { VisibilitySelector, type VisibilityType } from "./visibility-selector";
import { SaveGraphVersion } from "./save-graph-version";
import { ImageExport } from "./image-export";
import { JSONExport } from "./json-export";
import { useAtom } from "jotai";
import { graphNameAtom } from "@/lib/atoms";
import { ClearGraphCanvas } from "./clear-graph-canvas";

function PureChatHeader({
  chatId,
  selectedVisibilityType,
  isReadonly,
}: {
  chatId: string;
  selectedVisibilityType: VisibilityType;
  isReadonly: boolean;
}) {
  const router = useRouter();
  const [graphName, setGraphName] = useAtom(graphNameAtom);
  const { open } = useSidebar();

  const { width: windowWidth } = useWindowSize();

  return (
    <header className="sticky top-0 flex items-center gap-2 bg-background px-4 py-4 md:px-4 border-b-2 border-border">
      <SidebarToggle />

      {(!open || windowWidth < 768) && (
        <Button
          className="order-2 ml-auto h-8 px-2 md:order-1 md:ml-0 md:h-fit md:px-2"
          onClick={() => {
            router.push("/");
            router.refresh();
          }}
          variant="outline"
        >
          <PlusIcon />
          <span className="md:sr-only">New Chat</span>
        </Button>
      )}
      <SaveGraphVersion/>
      <ClearGraphCanvas/>
      <ImageExport/>
      <ImageExport download/>
      <JSONExport/>
      <JSONExport download/>

      {!isReadonly && (
        <VisibilitySelector
          chatId={chatId}
          className="order-1 md:order-1"
          selectedVisibilityType={selectedVisibilityType}
        />
      )}

      <div className="order-1 flex items-center justify-center w-2/3">
        <input
          type="text"
          value={graphName}
          onChange={(e) => {
            setGraphName(e.target.value);
          }}
          placeholder="Enter graph name"
          className={
            graphName.length > 0 ?
            "w-1/3 bg-transparent px-3 text-xl focus-visible:outline-none focus-visible:underline underline-offset-3 disabled:cursor-not-allowed md:text-xl" :
            "w-1/3 bg-transparent px-3 text-xl focus-visible:outline-none disabled:cursor-not-allowed md:text-xl"
          }
        />
      </div>

      {/* <Button
        asChild
        className="order-3 hidden bg-zinc-900 px-2 text-zinc-50 hover:bg-zinc-800 md:ml-auto md:flex md:h-fit dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200"
      >
        <Link
          href={"https://vercel.com/templates/next.js/nextjs-ai-chatbot"}
          rel="noreferrer"
          target="_noblank"
        >
          <VercelIcon size={16} />
          Deploy with Vercel
        </Link>
      </Button> */}
    </header>
  );
}

export const ChatHeader = memo(PureChatHeader, (prevProps, nextProps) => {
  return (
    prevProps.chatId === nextProps.chatId &&
    prevProps.selectedVisibilityType === nextProps.selectedVisibilityType &&
    prevProps.isReadonly === nextProps.isReadonly
  );
});
