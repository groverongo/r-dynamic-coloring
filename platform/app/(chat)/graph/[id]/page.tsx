import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import { auth } from "@/app/(auth)/auth";
import { GraphVisualize } from "@/components/chat";
import { DEFAULT_CHAT_MODEL } from "@/lib/ai/models";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/lib/queries";
import { GraphCanvasProvider } from "@/components/graphCanvas/useContext";
import { MainCanvasContext } from "@/lib/graph-constants";

export default async function Page(props: { params: Promise<{ id: string }> }) {
  const params = await props.params;
  const { id } = params;
  // const chat = await getChatById({ id });

  // if (!chat) {
  //   notFound();
  // }

  const session = await auth();

  if (!session) {
    redirect("/api/auth/guest");
  }

  // if (chat.visibility === "private") {
  //   if (!session.user) {
  //     return notFound();
  //   }

  //   if (session.user.id !== chat.userId) {
  //     return notFound();
  //   }
  // }

  // const messagesFromDb = await getMessagesByChatId({
  //   id,
  // });

  // const uiMessages = convertToUIMessages(messagesFromDb);

  const cookieStore = await cookies();
  const chatModelFromCookie = cookieStore.get("chat-model");

  if (!chatModelFromCookie) {
    return (
      <QueryClientProvider client={queryClient}>
        <GraphCanvasProvider context={MainCanvasContext}>

          <GraphVisualize
            autoResume={true}
            id={id}
            initialChatModel={DEFAULT_CHAT_MODEL}
            initialLastContext={undefined}
            // initialMessages={uiMessages}
            initialVisibilityType={"public"}
            isReadonly={false}
          />
        </GraphCanvasProvider>
      </QueryClientProvider>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <GraphCanvasProvider context={MainCanvasContext}>

        <GraphVisualize
          autoResume={true}
          id={id}
          initialChatModel={chatModelFromCookie.value}
          initialLastContext={undefined}
          // initialMessages={uiMessages}
          initialVisibilityType={"public"}
          isReadonly={false}
        />
      </GraphCanvasProvider>
    </QueryClientProvider>
  );
}
