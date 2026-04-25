"use client"

import { ChatHeader } from "@/components/chat-sidebar/chat-header"
import { ChatInput } from "@/components/chat-sidebar/chat-input"
import { ChatMessages } from "@/components/chat-sidebar/chat-messages"
import { Sidebar } from "@/components/ui/sidebar"
import { useState } from "react"

// Sample chat data
const initialMessages = [
  { role: "agent", content: "Hello! How can I help you today?" },
  { role: "user", content: "I need help with my project management." },
  { role: "agent", content: "Sure, I can help with that. What specifically do you need assistance with?" },
]

export function SidebarRight({
  ...props
}: React.ComponentProps<typeof Sidebar>) {
  const [messages, setMessages] = useState(initialMessages)

  const handleSendMessage = (content: string) => {
    setMessages([...messages, { role: "user", content }])

    // Simulate agent response
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { role: "agent", content: "I received your message: " + content },
      ])
    }, 1000)
  }

  return (
    <Sidebar
      collapsible="icon"
      side="right"
      className="sticky top-0 hidden h-svh border-l lg:flex"
      style={{
        "--sidebar-width": "24rem",
      } as React.CSSProperties}
      {...props}
    >
      <ChatHeader onNewConversation={() => setMessages([])} />
      <ChatMessages messages={messages} />
      <ChatInput onSend={handleSendMessage} />
    </Sidebar>
  )
}
