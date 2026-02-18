import { SidebarContent } from "@/components/ui/sidebar"

interface Message {
    role: string
    content: string
}

interface ChatMessagesProps {
    messages: Message[]
}

export function ChatMessages({ messages }: ChatMessagesProps) {
    return (
        <SidebarContent className="p-4">
            <div className="flex flex-col gap-4">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`flex w-full ${msg.role === "user" ? "justify-end" : "justify-start"
                            }`}
                    >
                        <div
                            className={`max-w-[85%] rounded-lg px-3 py-2 text-sm ${msg.role === "user"
                                    ? "bg-primary text-primary-foreground"
                                    : "bg-muted"
                                }`}
                        >
                            {msg.content}
                        </div>
                    </div>
                ))}
            </div>
        </SidebarContent>
    )
}
