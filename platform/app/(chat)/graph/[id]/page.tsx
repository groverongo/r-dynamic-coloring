import { Structure } from "@/components/structure";

export default async function Page(props: { params: Promise<{ id: string }> }) {
  const params = await props.params;
  const { id } = params;

  return (
    <Structure
      id={id}
      initialVisibilityType={"public"}
      isReadonly={false}
    />
  );
}
