import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { GraphVisualize } from "@/components/chat";
import { DEFAULT_CHAT_MODEL } from "@/lib/ai/models";
import { auth } from "../(auth)/auth";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/lib/queries";

export default async function Page() {
  const session = await auth();

  if (!session) {
    redirect("/api/auth/guest");
  }

  const cookieStore = await cookies();
  const modelIdFromCookie = cookieStore.get("chat-model");

  if (!modelIdFromCookie) {
    return (
      <QueryClientProvider client={queryClient}>
        <GraphVisualize
          autoResume={false}
          initialChatModel={DEFAULT_CHAT_MODEL}
          initialVisibilityType="private"
          isReadonly={false}
        />
      </QueryClientProvider>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <GraphVisualize
        autoResume={false}
        initialChatModel={modelIdFromCookie.value}
        initialVisibilityType="private"
        isReadonly={false}
      />
    </QueryClientProvider>
  );
}
