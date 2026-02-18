import { Button } from "@/components/ui/button"
import { SidebarFooter } from "@/components/ui/sidebar"
import { Textarea } from "@/components/ui/textarea"
import { Paperclip, Send } from "lucide-react"
import * as React from "react"

interface ChatInputProps {
    onSend: (message: string) => void
}

export function ChatInput({ onSend }: ChatInputProps) {
    const [inputValue, setInputValue] = React.useState("")

    const handleSendMessage = () => {
        if (!inputValue.trim()) return
        onSend(inputValue)
        setInputValue("")
    }

    return (
        <SidebarFooter className="p-4 pt-0">
            <div className="flex flex-col gap-2 rounded-lg border bg-background p-2 focus-within:ring-1 focus-within:ring-ring">
                <Textarea
                    placeholder="Type your message..."
                    className="min-h-12 resize-none border-0 p-0 shadow-none focus-visible:ring-0"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                            e.preventDefault()
                            handleSendMessage()
                        }
                    }}
                />
                <div className="flex items-center justify-between">
                    <Button variant="ghost" size="icon" className="h-8 w-8">
                        <Paperclip className="h-4 w-4" />
                        <span className="sr-only">Attach file</span>
                    </Button>
                    <Button size="sm" onClick={handleSendMessage} className="gap-2">
                        Send
                        <Send className="h-3.5 w-3.5" />
                    </Button>
                </div>
            </div>
        </SidebarFooter>
    )
}
