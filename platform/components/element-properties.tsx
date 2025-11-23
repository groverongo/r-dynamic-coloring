import { fontSizeAtom, nodeRadiusAtom } from "@/lib/atoms";
import { useAtom } from "jotai";
import { Info, SlidersVertical } from "lucide-react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "./ui/tooltip";
import { ChangeEventHandler } from "react";

function PropertyEntry({
    label,
    value,
    onChange,
    min,
    max,
    tooltip
}: {
    label: string;
    value: number;
    onChange: (value: number) => void;
    min: number;
    max: number;
    tooltip: string;
}){

    const handleValueChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = Number.parseInt(e.target.value, 10);
        if (!Number.isNaN(value) && value >= min && value <= max) {
            onChange(value);
        }
    };

    return (
        <div className="space-y-4">
            <div className="space-y-1">
                <div className="flex items-center justify-between">
                    <label htmlFor="node-radius" className="text-sm font-medium text-neutral-800 dark:text-neutral-200 flex items-center">
                        {label}
                        <TooltipProvider>
                            <Tooltip>
                                <TooltipTrigger asChild>
                                    <button className="ml-2 text-neutral-500 hover:text-neutral-700 dark:text-neutral-400 dark:hover:text-neutral-200">
                                        <Info className="h-4 w-4" />
                                    </button>
                                </TooltipTrigger>
                                <TooltipContent className="max-w-xs">
                                    <p>{tooltip}</p>
                                </TooltipContent>
                            </Tooltip>
                        </TooltipProvider>
                    </label>
                    <div className="relative">
                        <input
                            id="node-radius"
                            type="number"
                            min={min}
                            max={max}
                            value={value}
                            onChange={handleValueChange}
                            className="w-24 px-3 py-1.5 border border-neutral-300 dark:border-neutral-600 rounded-md text-right font-mono text-sm bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 focus:ring-2 focus:ring-neutral-500 focus:border-transparent transition-all"
                        />
                    </div>
                </div>
                <div className="flex justify-between text-xs text-neutral-500 dark:text-neutral-400 px-1">
                    <span>{min}</span>
                    <span>{max}</span>
                </div>
                <input
                    type="range"
                    min={min}
                    max={max}
                    value={value}
                    onChange={handleValueChange}
                    className="w-full h-2 bg-neutral-200 dark:bg-neutral-700 rounded-full appearance-none cursor-pointer accent-neutral-900 dark:accent-neutral-200"
                />
            </div>
        </div>
    );
}

export function EngineProperties() {
    const [nodeRadius, setNodeRadius] = useAtom(nodeRadiusAtom);
    const [fontSize, setFontSize] = useAtom(fontSizeAtom);

    return (
        <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg shadow-sm border border-neutral-200 dark:border-neutral-800 p-4 w-full max-w-md">
            <h3 className="text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-4 flex items-center">
                <span className="bg-neutral-100 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 border border-neutral-300 dark:border-neutral-600 rounded-full w-8 h-8 flex items-center justify-center mr-3 text-sm font-mono"><SlidersVertical/></span>
                Engine Properties
            </h3>

            <PropertyEntry
                label="Node Radius"
                value={nodeRadius}
                onChange={setNodeRadius}
                min={2}
                max={100}
                tooltip="Set the radius of vertices in the graph"
            />
            
            <PropertyEntry
                label="Font Size"
                value={fontSize}
                onChange={setFontSize}
                min={2}
                max={100}
                tooltip="Set the font size of vertices in the graph"
            />
        </div>
    );
}