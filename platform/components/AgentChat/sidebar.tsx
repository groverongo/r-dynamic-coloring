"use client";

import { Sidebar, SidebarContent, SidebarFooter, SidebarHeader, SidebarMenu } from "@/components/ui/sidebar";
import { MainCanvasContext } from "@/lib/graph-constants";
import { GraphSerializer } from "@/lib/serializers";
import { useGraphCanvasContext } from "@r-dynamic-coloring/graph-canvas";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { useState } from "react";
import { v4 as uuidv4 } from 'uuid';
import z from "zod";
import { ChatAgentContent, CustomMessage } from "./content";
import { ChatContext } from "./context";
import { Prompter } from "./prompt";
import { Title } from "./title";

export function AgentChatSidebar() {

    const {
        graphAdjacencyList,
    } = useGraphCanvasContext(MainCanvasContext);
    const [input, setInput] = useState<string>("");
    const [messages, setMessages] = useState<CustomMessage[]>([]);

    const { isSuccess, error, mutateAsync, data, isPending } = useMutation({
        mutationFn: async () => {
            const responseSchema = z.object({
                answer: z.string(),
            });

            const response = await axios.post(`${process.env.NEXT_PUBLIC_R_HUED_COLORING_API}/agent`, {
                graph: JSON.parse(GraphSerializer.simpleGraphAdjacencyListSerializer(graphAdjacencyList)),
                prompt: input,
            });

            const data = responseSchema.parse(response.data);
            return data;
        },
        retry: false
    });

    const callAgent = () => {
        console.log(graphAdjacencyList, input, MainCanvasContext)
        if (graphAdjacencyList.size === 0) return;
        if (!input.trim()) return;
        setMessages((prev) => [...prev, { type: 'request', data: input, timestamp: new Date().toISOString(), id: uuidv4() }]);
        mutateAsync().then((data) => {
            setMessages((prev) => [...prev, { type: 'response', data: data.answer, timestamp: new Date().toISOString(), id: uuidv4() }]);
            setInput("");
        }).catch((error) => {
            setMessages((prev) => prev.slice(0, -1));
            console.error(error);
        });
    }

    return (
        <ChatContext.Provider value={{ input, setInput, messages, setMessages, isPending, callAgent }}>

            <Sidebar collapsible="none" style={{
                "--sidebar-width": "35rem",
                "--sidebar-width-mobile": "35rem",
            }} side="right" className="hidden md:flex h-svh sticky top-0 group-data-[side=right]:border-l-0">
                <SidebarHeader>
                    <SidebarMenu>
                        <Title />
                    </SidebarMenu>
                </SidebarHeader>
                <SidebarContent>
                    <ChatAgentContent />
                </SidebarContent>
                <SidebarFooter>
                    <Prompter />
                </SidebarFooter>
            </Sidebar>
        </ChatContext.Provider>

    );
}