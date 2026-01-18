import { Structure } from "@/components/structure";

export default async function Page() {

  return (
    <Structure
      initialVisibilityType="private"
      isReadonly={false}
    />
  );
}
