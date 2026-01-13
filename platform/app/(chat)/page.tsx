import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { Structure } from "@/components/structure";
import { DEFAULT_CHAT_MODEL } from "@/lib/ai/models";
import { auth } from "../(auth)/auth";

export default async function Page() {
  const session = await auth();

  if (!session) {
    redirect("/api/auth/guest");
  }

  const cookieStore = await cookies();
  const modelIdFromCookie = cookieStore.get("chat-model");

  if (!modelIdFromCookie) {
    return (
      <Structure
        autoResume={false}
        initialChatModel={DEFAULT_CHAT_MODEL}
        initialVisibilityType="private"
        isReadonly={false}
      />
    );
  }

  return (
    <Structure
      autoResume={false}
      initialChatModel={modelIdFromCookie.value}
      initialVisibilityType="private"
      isReadonly={false}
    />
  );
}
