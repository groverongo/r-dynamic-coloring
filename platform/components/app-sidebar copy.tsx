"use client";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  useSidebar,
} from "@/components/ui/sidebar";
import { MainCanvasContext } from "@/lib/graph-constants";
import { queryClient } from "@/lib/queries";
import { GraphCanvasProvider } from "@r-dynamic-coloring/graph-canvas";
import { QueryClientProvider } from "@tanstack/react-query";
import { Dispatch, SetStateAction } from "jotai";
import { Send } from "lucide-react";
import type { User } from "next-auth";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { createContext, useContext, useState } from "react";
import { toast } from "sonner";
import { useSWRConfig } from "swr";
import { ChatAgentContent } from "./chat-agent";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "./ui/alert-dialog";

interface CustomMessage {
  type: 'request' | 'response';
  data: string;
  timestamp: string;
  id: string;
}

type ChatContextType = {
  input: string;
  setInput: Dispatch<SetStateAction<string>>;
  messages: CustomMessage[];
  setMessages: Dispatch<SetStateAction<CustomMessage[]>>;
}
const ChatContext = createContext<ChatContextType | null>(null);

export const useChatContext = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error("useChatContext must be used within ChatProvider");
  }
  return context;
}

export function ChatAgentSidebar({ user }: { user: User | undefined }) {
  const router = useRouter();
  const { setOpenMobile } = useSidebar();
  const { mutate } = useSWRConfig();
  const [showDeleteAllDialog, setShowDeleteAllDialog] = useState(false);


  const [input, setInput] = useState<string>("");
  const [messages, setMessages] = useState<CustomMessage[]>([]);

  const handleDeleteAll = () => {
    const deletePromise = fetch("/api/history", {
      method: "DELETE",
    });

    toast.promise(deletePromise, {
      loading: "Deleting all chats...",
      success: () => {
        // mutate(unstable_serialize(getChatHistoryPaginationKey));
        router.push("/");
        setShowDeleteAllDialog(false);
        return "All chats deleted successfully";
      },
      error: "Failed to delete all chats",
    });
  };

  return (
    <QueryClientProvider client={queryClient}>
      <GraphCanvasProvider context={MainCanvasContext}>
        <ChatContext.Provider value={{ input, setInput, messages, setMessages }}>
          <Sidebar collapsible="none" style={{
            "--sidebar-width": "35rem",
            "--sidebar-width-mobile": "35rem",
          }} side="right" className="hidden md:flex h-svh sticky top-0 group-data-[side=right]:border-l-0">
            <SidebarHeader>
              <SidebarMenu>
                <div className="flex flex-row items-center justify-between">
                  <Link
                    className="flex flex-row items-center gap-3"
                    href="/"
                    onClick={() => {
                      setOpenMobile(false);
                    }}
                  >
                    <span className="cursor-pointer rounded-md px-2 my-3 font-semibold text-xl hover:bg-muted">
                      Chat with Dynamax
                    </span>
                  </Link>

                </div>
              </SidebarMenu>
            </SidebarHeader>
            <SidebarContent>
              <ChatAgentContent />
            </SidebarContent>
            <SidebarFooter>
              <div className="sticky bottom-0 z-1 mx-auto flex w-full max-w-4xl gap-2 border-t-0  px-2 pb-3 md:px-4 md:pb-4">

                <input
                  type="text"
                  value={chatAgentRef.current?.input}
                  onChange={(e) => {
                    console.log(e.target.value, chatAgentRef.current?.input, chatAgentRef.current?.isPending);
                    chatAgentRef.current?.setInput(e.target.value)
                  }}
                  onKeyDown={(e) => e.key === 'Enter' && chatAgentRef.current?.callAgent()}
                  placeholder="Type your message..."
                  className="flex-1 px-4 py-2 border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-500"
                  disabled={chatAgentRef.current?.isPending}
                />
                <button
                  onClick={() => chatAgentRef.current?.callAgent()}
                  disabled={chatAgentRef.current?.isPending || !chatAgentRef.current?.input.trim()}
                  className="px-6 py-2 bg-neutral-600 text-white rounded-lg hover:bg-neutral-700 disabled:bg-neutral-300 disabled:cursor-not-allowed flex items-center gap-2 transition-colors"
                >
                  <Send className="w-4 h-4" />
                  Send
                </button>
              </div>
            </SidebarFooter>
          </Sidebar>
        </ChatContext.Provider>

        <AlertDialog onOpenChange={setShowDeleteAllDialog} open={showDeleteAllDialog}>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Delete all chats?</AlertDialogTitle>
              <AlertDialogDescription>
                This action cannot be undone. This will permanently delete all your
                chats and remove them from our servers.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogAction onClick={handleDeleteAll}>
                Delete All
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
      </GraphCanvasProvider>
    </QueryClientProvider>
  );
}
