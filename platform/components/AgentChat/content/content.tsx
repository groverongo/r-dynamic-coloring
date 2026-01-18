"use client";

import { MainCanvasContext } from "@/lib/graph-constants";
import { useGraphCanvasContext } from "@r-dynamic-coloring/graph-canvas";
import { Bot, User } from "lucide-react";
import ReactMarkdown from 'react-markdown';
import { useChatContext } from "../context";
import { CustomMessage } from "./types";


const renderRequest = (message: CustomMessage) => (
    <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg p-4 space-y-2">
        <div className="flex items-start gap-3">
            <User className="w-5 h-5 text-neutral-600 dark:text-neutral-400 mt-1" />
            <div className="flex-1">
                <div className="prose prose-sm max-w-none text-neutral-900 dark:text-neutral-100 font-medium text-sm ">
                    <ReactMarkdown>{message.data}</ReactMarkdown>
                </div>
                <div className="mt-2 text-xs text-neutral-600 dark:text-neutral-400 space-y-1">
                    <div><span className="font-semibold">Timestamp:</span> {new Date(message.timestamp).toLocaleString()}</div>
                </div>
            </div>
        </div>
    </div>
);

const renderResponse = (message: CustomMessage) => (
    <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg p-4 space-y-2">
        <div className="flex items-start gap-3">
            <Bot className="w-5 h-5 text-neutral-700 dark:text-neutral-400 mt-1" />
            <div className="flex-1">
                <div className="prose-sm max-w-none text-neutral-900 dark:text-neutral-100 font-medium text-sm ">
                    <ReactMarkdown>{message.data}</ReactMarkdown>
                </div>
                <div className="mt-2 text-xs text-neutral-600 dark:text-neutral-400 space-y-1">
                    <div><span className="font-semibold">Timestamp:</span> {new Date(message.timestamp).toLocaleString()}</div>
                </div>
            </div>
        </div>
    </div>
);


export function ChatAgentContent() {

    const { messages, isPending } = useChatContext();


    const {
        graphAdjacencyList,
    } = useGraphCanvasContext(MainCanvasContext);

    return (
        <>
            <div
                className="overscroll-behavior-contain -webkit-overflow-scrolling-touch flex-1 touch-pan-y overflow-y-scroll"
            >
                {messages.map((message) => (
                    <div key={message.id} className="mb-2 ml-2 mr-2">
                        {message.type === 'request'
                            ? renderRequest(message)
                            : renderResponse(message)
                        }
                    </div>
                ))}

                {isPending && (
                    <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg p-4 mb-2 ml-2 mr-2">
                        <div className="flex items-center gap-3">
                            <Bot className="w-5 h-5 text-neutral-700 dark:text-neutral-400 animate-pulse" />
                            <div className="flex gap-1">
                                <span className="w-2 h-2 bg-neutral-400 dark:bg-neutral-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                                <span className="w-2 h-2 bg-neutral-400 dark:bg-neutral-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                                <span className="w-2 h-2 bg-neutral-400 dark:bg-neutral-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </>
    );
}
