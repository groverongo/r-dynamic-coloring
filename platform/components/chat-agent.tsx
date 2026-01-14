"use client";

import { MainCanvasContext } from "@/lib/graph-constants";
import { GraphSerializer } from "@/lib/serializers";
import { useGraphCanvasContext } from "@r-dynamic-coloring/graph-canvas";
import { useMutation } from '@tanstack/react-query';
import axios from "axios";
import { Bot, Send, User } from "lucide-react";
import { useState } from "react";
import ReactMarkdown from 'react-markdown';
import { v4 as uuidv4 } from 'uuid';
import z from "zod";

interface CustomMessage {
  type: 'request' | 'response';
  data: string;
  timestamp: string;
  id: string;
}

export function ChatAgent() {
  const [input, setInput] = useState<string>("");
  const [messages, setMessages] = useState<CustomMessage[]>([]);

  const {
    graphAdjacencyList,
  } = useGraphCanvasContext(MainCanvasContext);

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
    <>
      <div className="flex border-t-0 px-2 pb-3 pt-3 md:px-4 md:pb-3 md:pt-3">
        <p className="text-lg font-semibold">Chat with Dynamax</p>
      </div>
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
      <div className="sticky bottom-0 z-1 mx-auto flex w-full max-w-4xl gap-2 border-t-0 bg-background px-2 pb-3 md:px-4 md:pb-4">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && callAgent()}
          placeholder="Type your message..."
          className="flex-1 px-4 py-2 border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-500"
          disabled={isPending}
        />
        <button
          onClick={callAgent}
          disabled={isPending || !input.trim()}
          className="px-6 py-2 bg-neutral-600 text-white rounded-lg hover:bg-neutral-700 disabled:bg-neutral-300 disabled:cursor-not-allowed flex items-center gap-2 transition-colors"
        >
          <Send className="w-4 h-4" />
          Send
        </button>
      </div>
    </>
  );
}
