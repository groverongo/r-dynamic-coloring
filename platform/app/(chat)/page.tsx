import { Structure } from "@/components/structure";
import { DEFAULT_CHAT_MODEL } from "@/lib/ai/models";

export default async function Page() {

  return (
    <Structure
      initialChatModel={DEFAULT_CHAT_MODEL}
      initialVisibilityType="private"
      isReadonly={false}
    />
  );
}
