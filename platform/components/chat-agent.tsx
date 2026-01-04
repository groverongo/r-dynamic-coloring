"use client";

import { useState } from "react";
import { useMutation } from '@tanstack/react-query';
import { GraphSerializer } from "@/lib/serializers";
import { useAtomValue } from "jotai";
import { graphAdjacencyListAtom } from "@/lib/atoms";
import axios from "axios";
import z from "zod";
import { Bot, User } from "lucide-react";
import { v4 as uuidv4 } from 'uuid';

interface CustomMessage {
  type: 'request' | 'response';
  data: string;
  timestamp: string;
  id: string;
}

export function ChatAgent() {
  const [input, setInput] = useState<string>("");
  const [messages, setMessages] = useState<CustomMessage[]>([]);

  const graphAdjacencyList = useAtomValue(graphAdjacencyListAtom);

  const renderRequest = (message: CustomMessage) => (
    <div className="bg-blue-50 rounded-lg p-4 space-y-2">
      <div className="flex items-start gap-3">
        <User className="w-5 h-5 text-blue-600 mt-1" />
        <div className="flex-1">
          <p className="text-gray-900 font-medium">{message.data}</p>
          <div className="mt-2 text-xs text-gray-600 space-y-1">
            <div><span className="font-semibold">Timestamp:</span> {new Date(message.timestamp).toLocaleString()}</div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderResponse = (message: CustomMessage) => (
    <div className="bg-gray-50 rounded-lg p-4 space-y-2">
      <div className="flex items-start gap-3">
        <Bot className="w-5 h-5 text-gray-700 mt-1" />
        <div className="flex-1">
          <p className="text-gray-900">{message.data}</p>
          <div className="mt-2 text-xs text-gray-600 space-y-1">
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

      const response = await axios.post(`${process.env.NEXT_PUBLIC_R_HUED_COLORING_AGENT}/invoke`, {
        graph: JSON.parse(GraphSerializer.simpleGraphAdjacencyListSerializer(graphAdjacencyList)),
        prompt: input,
      });

      const data = responseSchema.parse(response.data);
      return data;
    },
    retry: false
  });


  return (
    <>
      <div
        className="overscroll-behavior-contain -webkit-overflow-scrolling-touch flex-1 touch-pan-y overflow-y-scroll"
      >
        {messages.map((message) => (
          <div key={message.id}>
            {message.type === 'request'
              ? renderRequest(message)
              : renderResponse(message)
            }
          </div>
        ))}
      </div>
      <div className="sticky bottom-0 z-1 mx-auto flex w-full max-w-4xl gap-2 border-t-0 bg-background px-2 pb-3 md:px-4 md:pb-4">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          // onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type your message..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        // disabled={isLoading}
        />
        <button
          onClick={() => {
            setMessages((prev) => [...prev, { type: 'request', data: input, timestamp: new Date().toISOString(), id: uuidv4() }]);
            mutateAsync().then((data) => {
              setMessages((prev) => [...prev, { type: 'response', data: data.answer, timestamp: new Date().toISOString(), id: uuidv4() }]);
            }).catch((error) => {
              console.error(error);
            });
          }}
          // onClick={handleSend}
          // disabled={isLoading || !input.trim()}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center gap-2 transition-colors"
        >
          {/* <Send className="w-4 h-4" /> */}
          Send
        </button>
      </div>
    </>
  );
}
