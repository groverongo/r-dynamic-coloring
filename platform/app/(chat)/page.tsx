import { Structure } from "@/components/structure";
import { DEFAULT_CHAT_MODEL } from "@/lib/ai/models";
import { cookies } from "next/headers";

export default async function Page() {

  const cookieStore = await cookies();
  const modelIdFromCookie = cookieStore.get("chat-model");

  return (
    <Structure
      autoResume={false}
      initialChatModel={DEFAULT_CHAT_MODEL}
      initialVisibilityType="private"
      isReadonly={false}
    />
  );
}
