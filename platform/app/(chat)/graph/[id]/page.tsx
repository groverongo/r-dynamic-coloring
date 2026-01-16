import { Structure } from "@/components/structure";
import { DEFAULT_CHAT_MODEL } from "@/lib/ai/models";

export default async function Page(props: { params: Promise<{ id: string }> }) {
  const params = await props.params;
  const { id } = params;

  return (
    <Structure
      id={id}
      initialChatModel={DEFAULT_CHAT_MODEL}
      initialVisibilityType={"public"}
      isReadonly={false}
    />
  );
}
