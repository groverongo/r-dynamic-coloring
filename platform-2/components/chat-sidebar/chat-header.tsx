import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import { SidebarHeader } from "@/components/ui/sidebar"
import { MessageSquare, Plus } from "lucide-react"
import { NavUser } from "../nav-user"

const pastConversations = [
    { id: "1", title: "Project Planning", date: "2023-10-25" },
    { id: "2", title: "Bug Fixing", date: "2023-10-24" },
    { id: "3", title: "Feature Request", date: "2023-10-23" },
]

const data = {
    user: {
        name: "shadcn",
        email: "m@example.com",
        avatar: "/avatars/shadcn.jpg",
    },
    calendars: [
        {
            name: "My Calendars",
            items: ["Personal", "Work", "Family"],
        },
        {
            name: "Favorites",
            items: ["Holidays", "Birthdays"],
        },
        {
            name: "Other",
            items: ["Travel", "Reminders", "Deadlines"],
        },
    ],
}

interface ChatHeaderProps {
    onNewConversation: () => void
}

export function ChatHeader({ onNewConversation }: ChatHeaderProps) {
    return (
        <SidebarHeader className="border-sidebar-border h-auto border-b flex flex-col gap-4 p-4">
            <NavUser user={data.user} />
            <Separator />
            <div className="flex w-full items-center justify-between">
                <span className="font-semibold text-sm">AI Assistant</span>
                <div className="flex gap-2">
                    <Button
                        variant="ghost"
                        size="icon"
                        title="New Conversation"
                        onClick={onNewConversation}
                    >
                        <Plus className="h-4 w-4" />
                    </Button>
                    <Dialog>
                        <DialogTrigger asChild>
                            <Button variant="ghost" size="icon" title="History">
                                <MessageSquare className="h-4 w-4" />
                            </Button>
                        </DialogTrigger>
                        <DialogContent>
                            <DialogHeader>
                                <DialogTitle>Past Conversations</DialogTitle>
                                <DialogDescription>
                                    Select a conversation to view.
                                </DialogDescription>
                            </DialogHeader>
                            <ScrollArea className="h-[300px] w-full rounded-md border p-4">
                                <div className="flex flex-col gap-2">
                                    {pastConversations.map((chat) => (
                                        <Button
                                            key={chat.id}
                                            variant="ghost"
                                            className="justify-start w-full text-left"
                                        >
                                            <div className="flex flex-col items-start gap-1">
                                                <span className="font-medium">{chat.title}</span>
                                                <span className="text-xs text-muted-foreground">
                                                    {chat.date}
                                                </span>
                                            </div>
                                        </Button>
                                    ))}
                                </div>
                            </ScrollArea>
                        </DialogContent>
                    </Dialog>
                </div>
            </div>
        </SidebarHeader>
    )
}
