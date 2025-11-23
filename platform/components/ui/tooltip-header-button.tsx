import { Tooltip } from "radix-ui";
import "../../styles/IOHeaderButtons.css";

export function TooltipHeaderButton({ children, tooltipContent }: { children: React.ReactNode, tooltipContent: string }) {
  return (
    <Tooltip.Provider>
        <Tooltip.Root>
            <Tooltip.Trigger asChild>
                {children}
            </Tooltip.Trigger>
            <Tooltip.Portal>
                <Tooltip.Content className="TooltipContent" side="bottom" sideOffset={5}>
                    {tooltipContent}
                <Tooltip.Arrow className="TooltipArrow" />
                </Tooltip.Content>
            </Tooltip.Portal>
        </Tooltip.Root>
    </Tooltip.Provider>   
  )
}