"use client";

import { isToday, isYesterday, subMonths, subWeeks } from "date-fns";
import { motion } from "framer-motion";
import { useParams, useRouter } from "next/navigation";
import type { User } from "next-auth";
import { useEffect, useRef, useState } from "react";
import { toast } from "sonner";
import useSWRInfinite from "swr/infinite";
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
import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  useSidebar,
} from "@/components/ui/sidebar";
import type { Chat } from "@/lib/db/schema";
import { fetcher } from "@/lib/utils";
import { LoaderIcon } from "./icons";
import { GraphItem } from "./sidebar-history-item";
import { useMutation, useQuery } from "@tanstack/react-query";
import axios from "axios";
import { GraphsResponse } from "@/lib/validation";
import { Toast } from "radix-ui";

import "../styles/SaveGraphVersion.css";

type GroupedGraphs = {
  today: GraphsResponse[];
  yesterday: GraphsResponse[];
  lastWeek: GraphsResponse[];
  lastMonth: GraphsResponse[];
  older: GraphsResponse[];
};

const ToastConditionComponents = {
  success: {
    title: <Toast.Title className="ToastTitle text-zinc-900 dark:text-zinc-200">The following graph has been deleted 😄</Toast.Title>,
    description: (savedGraphId: string) => <Toast.Description className="ToastDescription">{savedGraphId}</Toast.Description>,
  },
  failure: {
    title: <Toast.Title className="ToastTitle text-zinc-900 dark:text-zinc-200">Failed to delete graph 😭</Toast.Title>,
    description: (errorMessage: string) => <Toast.Description className="ToastDescription">{errorMessage}</Toast.Description>,
  }
}

export type GraphsHistory = {
  graphs: GraphsResponse[];
  hasMore: boolean;
};

const PAGE_SIZE = 20;

const groupGraphsByDate = (graphs: GraphsResponse[]): GroupedGraphs => {
  const now = new Date();
  const oneWeekAgo = subWeeks(now, 1);
  const oneMonthAgo = subMonths(now, 1);

  return graphs.reduce(
    (groups, chat) => {
      const chatDate = new Date(chat.createdAt);

      if (isToday(chatDate)) {
        groups.today.push(chat);
      } else if (isYesterday(chatDate)) {
        groups.yesterday.push(chat);
      } else if (chatDate > oneWeekAgo) {
        groups.lastWeek.push(chat);
      } else if (chatDate > oneMonthAgo) {
        groups.lastMonth.push(chat);
      } else {
        groups.older.push(chat);
      }

      return groups;
    },
    {
      today: [],
      yesterday: [],
      lastWeek: [],
      lastMonth: [],
      older: [],
    } as GroupedGraphs
  );
};

export function SidebarHistory({ user }: { user: User | undefined }) {
  const { setOpenMobile } = useSidebar();
  const { id } = useParams();
  const [pageIndex, setPageIndex] = useState(0);

  const timerRef = useRef<NodeJS.Timeout>();
  const [open, setOpen] = useState(false);

  const { data: paginatedGraphsHistory, isLoading: graphsLoading, refetch: fetchGraphs } = useQuery({
    queryKey: ["graphs", pageIndex],
    queryFn: async () => {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_R_HUED_COLORING_API}/graphs?limit=${PAGE_SIZE}`
      );
      if(response.data?.graphs === null) 
        response.data.graphs = [];

      console.log("Processed graphs:", response.data);
      return response.data as GraphsHistory;
    },
    refetchOnMount: false,
    retry: false,
  });

  const {mutate: deleteGraph, isSuccess: deleteGraphSuccess, error: deleteGraphError} = useMutation({
    mutationFn: async () => {
      const response = await axios.delete(
        `${process.env.NEXT_PUBLIC_R_HUED_COLORING_API}/graphs/${id}`
      );
      return response.data;
    },
    retry: false,
    onSuccess: () => {
      if(id === deleteId)
          router.push("/");
    },
    onError: () => {
      toast("Failed to delete graph");
    }
  });

  const deleteSpecificGraph = () => {
    deleteGraph();

    setOpen(false);
    globalThis.clearTimeout(timerRef.current);
    timerRef.current = globalThis.setTimeout(() => {
      setOpen(true);
    }, 100);
  }
  
  const router = useRouter();
  const [deleteId, setDeleteId] = useState<string | null>(null);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);

  const hasReachedEnd = paginatedGraphsHistory?.graphs
    ? paginatedGraphsHistory.hasMore === false
    : false;

  const hasEmptyGraphsHistory = paginatedGraphsHistory?.graphs
    ? paginatedGraphsHistory.graphs.length === 0
    : false;

  if (!user) {
    return (
      <SidebarGroup>
        <SidebarGroupContent>
          <div className="flex w-full flex-row items-center justify-center gap-2 px-2 text-sm text-zinc-500">
            Login to save and revisit previous chats!
          </div>
        </SidebarGroupContent>
      </SidebarGroup>
    );
  }

  if (graphsLoading) {
    return (
      <SidebarGroup>
        <div className="px-2 py-1 text-sidebar-foreground/50 text-xs">
          Today
        </div>
        <SidebarGroupContent>
          <div className="flex flex-col">
            {[44, 32, 28, 64, 52].map((item) => (
              <div
                className="flex h-8 items-center gap-2 rounded-md px-2"
                key={item}
              >
                <div
                  className="h-4 max-w-(--skeleton-width) flex-1 rounded-md bg-sidebar-accent-foreground/10"
                  style={
                    {
                      "--skeleton-width": `${item}%`,
                    } as React.CSSProperties
                  }
                />
              </div>
            ))}
          </div>
        </SidebarGroupContent>
      </SidebarGroup>
    );
  }

  if (hasEmptyGraphsHistory) {
    return (
      <SidebarGroup>
        <SidebarGroupContent>
          <div className="flex w-full flex-row items-center justify-center gap-2 px-2 text-sm text-zinc-500">
            Your conversations will appear here once you start chatting!
          </div>
        </SidebarGroupContent>
      </SidebarGroup>
    );
  }

  return (
    <>
      <SidebarGroup>
        <SidebarGroupContent>
          <SidebarMenu>
            {paginatedGraphsHistory &&
              (() => {
                const graphsFromHistory = paginatedGraphsHistory.graphs;

                const groupedGraphs = groupGraphsByDate(graphsFromHistory);

                return (
                  <div className="flex flex-col gap-6">
                    {groupedGraphs.today.length > 0 && (
                      <div>
                        <div className="px-2 py-1 text-sidebar-foreground/50 text-xs">
                          Today
                        </div>
                        {groupedGraphs.today.map((graph) => (
                          <Toast.Provider swipeDirection="right">
                            <GraphItem
                              graph={graph}
                              isActive={graph.id === id}
                              key={graph.id}
                              onDelete={(graphId) => {
                                setDeleteId(graphId);
                                setShowDeleteDialog(true);
                              }}
                              setOpenMobile={setOpenMobile}
                            />
                            <Toast.Root className="ToastRoot bg-neutral-50 dark:bg-neutral-900 border border-emerald-200 dark:border-emerald-800" open={open} onOpenChange={setOpen}>
                              {ToastConditionComponents[deleteGraphSuccess ? "success" : "failure"].title}
                              {ToastConditionComponents[deleteGraphSuccess ? "success" : "failure"].description(deleteGraphSuccess ? graph.id : JSON.stringify(deleteGraphError))}
                            </Toast.Root>
                            <Toast.Viewport className="ToastViewport" />
                          </Toast.Provider>
                        ))}
                      </div>
                    )}

                    {groupedGraphs.yesterday.length > 0 && (
                      <div>
                        <div className="px-2 py-1 text-sidebar-foreground/50 text-xs">
                          Yesterday
                        </div>
                        {groupedGraphs.yesterday.map((graph) => (
                          <GraphItem
                            graph={graph}
                            isActive={graph.id === id}
                            key={graph.id}
                            onDelete={(graphId) => {
                              setDeleteId(graphId);
                              setShowDeleteDialog(true);
                            }}
                            setOpenMobile={setOpenMobile}
                          />
                        ))}
                      </div>
                    )}

                    {groupedGraphs.lastWeek.length > 0 && (
                      <div>
                        <div className="px-2 py-1 text-sidebar-foreground/50 text-xs">
                          Last 7 days
                        </div>
                        {groupedGraphs.lastWeek.map((graph) => (
                          <GraphItem
                            graph={graph}
                            isActive={graph.id === id}
                            key={graph.id}
                            onDelete={(graphId) => {
                              setDeleteId(graphId);
                              setShowDeleteDialog(true);
                            }}
                            setOpenMobile={setOpenMobile}
                          />
                        ))}
                      </div>
                    )}

                    {groupedGraphs.lastMonth.length > 0 && (
                      <div>
                        <div className="px-2 py-1 text-sidebar-foreground/50 text-xs">
                          Last 30 days
                        </div>
                        {groupedGraphs.lastMonth.map((graph) => (
                          <GraphItem
                            graph={graph}
                            isActive={graph.id === id}
                            key={graph.id}
                            onDelete={(graphId) => {
                              setDeleteId(graphId);
                              setShowDeleteDialog(true);
                            }}
                            setOpenMobile={setOpenMobile}
                          />
                        ))}
                      </div>
                    )}

                    {groupedGraphs.older.length > 0 && (
                      <div>
                        <div className="px-2 py-1 text-sidebar-foreground/50 text-xs">
                          Older than last month
                        </div>
                        {groupedGraphs.older.map((graph) => (
                          <GraphItem
                            graph={graph}
                            isActive={graph.id === id}
                            key={graph.id}
                            onDelete={(graphId) => {
                              setDeleteId(graphId);
                              setShowDeleteDialog(true);
                            }}
                            setOpenMobile={setOpenMobile}
                          />
                        ))}
                      </div>
                    )}
                  </div>
                );
              })()}
          </SidebarMenu>

          {hasReachedEnd ? (
            <div className="mt-8 flex w-full flex-row items-center justify-center gap-2 px-2 text-sm text-zinc-500">
              You have reached the end of your chat history.
            </div>
          ) : (
            <div className="mt-8 flex flex-row items-center gap-2 p-2 text-zinc-500 dark:text-zinc-400">
              <div className="animate-spin">
                <LoaderIcon />
              </div>
              <div>Loading Chats...</div>
            </div>
          )}
        </SidebarGroupContent>
      </SidebarGroup>

      <AlertDialog onOpenChange={setShowDeleteDialog} open={showDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete your
              chat and remove it from our servers.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={deleteSpecificGraph}>
              Continue
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
