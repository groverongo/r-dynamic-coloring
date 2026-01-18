"use client";

import { Send } from "lucide-react";
import { useChatContext } from "./context";


export function Prompter() {

    const { input, setInput, callAgent, isPending } = useChatContext();


    return (
        <div className="sticky bottom-0 z-1 mx-auto flex w-full max-w-4xl gap-2 border-t-0  px-2 pb-3 md:px-4 md:pb-4">

            <input
                type="text"
                value={input}
                onChange={(e) => {
                    setInput(e.target.value)
                }}
                onKeyDown={(e) => e.key === 'Enter' && callAgent()}
                placeholder="Type your message..."
                className="flex-1 px-4 py-2 border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-500"
                disabled={isPending}
            />
            <button
                onClick={() => callAgent()}
                disabled={isPending || !input.trim()}
                className="px-6 py-2 bg-neutral-600 text-white rounded-lg hover:bg-neutral-700 disabled:bg-neutral-300 disabled:cursor-not-allowed flex items-center gap-2 transition-colors"
            >
                <Send className="w-4 h-4" />
                Send
            </button>
        </div>
    );
}