import { kColorsAtom, rFactorAtom } from "@/lib/atoms";
import { useAtom } from "jotai";
import { Info, Palette } from "lucide-react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "./ui/tooltip";

export function ColoringParameters() {
    const [kColors, setKColors] = useAtom(kColorsAtom);
    const [rFactor, setRFactor] = useAtom(rFactorAtom);

    const handleRFactorChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = Number.parseInt(e.target.value, 10);
        if (!Number.isNaN(value) && value >= 1) {
            setRFactor(value);
        }
    };

    const handleKColorsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = Number.parseInt(e.target.value, 10);
        if (!Number.isNaN(value) && value >= 2) {
            setKColors(value);
        }
    };

    return (
        <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg shadow-sm border border-neutral-200 dark:border-neutral-800 p-4 w-full max-w-md">
            <h3 className="text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-4 flex items-center">
                <span className="bg-neutral-100 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 border border-neutral-300 dark:border-neutral-600 rounded-full w-8 h-8 flex items-center justify-center mr-3 text-sm font-mono"><Palette/></span>
                Coloring Parameters
            </h3>
            
            <div className="space-y-4">
                <div className="space-y-1">
                    <div className="flex items-center justify-between">
                        <label htmlFor="k-colors" className="text-sm font-medium text-neutral-800 dark:text-neutral-200 flex items-center">
                            Number of Colors (k)
                            <TooltipProvider>
                                <Tooltip>
                                    <TooltipTrigger asChild>
                                        <button className="ml-2 text-neutral-500 hover:text-neutral-700 dark:text-neutral-400 dark:hover:text-neutral-200">
                                            <Info className="h-4 w-4" />
                                        </button>
                                    </TooltipTrigger>
                                    <TooltipContent className="max-w-xs">
                                        <p>Set the maximum number of colors to use for graph coloring (2-10)</p>
                                    </TooltipContent>
                                </Tooltip>
                            </TooltipProvider>
                        </label>
                        <div className="relative">
                            <input
                                id="k-colors"
                                type="number"
                                min="2"
                                max="10"
                                value={kColors}
                                onChange={handleKColorsChange}
                                className="w-24 px-3 py-1.5 border border-neutral-300 dark:border-neutral-600 rounded-md text-right font-mono text-sm bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 focus:ring-2 focus:ring-neutral-500 focus:border-transparent transition-all"
                            />
                            <span className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-500 dark:text-neutral-400 text-sm pointer-events-none">
                                {kColors}
                            </span>
                        </div>
                    </div>
                    <div className="flex justify-between text-xs text-neutral-500 dark:text-neutral-400 px-1">
                        <span>2</span>
                        <span>10</span>
                    </div>
                    <input
                        type="range"
                        min="2"
                        max="10"
                        value={kColors}
                        onChange={handleKColorsChange}
                        className="w-full h-2 bg-neutral-200 dark:bg-neutral-700 rounded-full appearance-none cursor-pointer accent-neutral-900 dark:accent-neutral-200"
                    />
                </div>

                <div className="space-y-1">
                    <div className="flex items-center justify-between">
                        <label htmlFor="r-factor" className="text-sm font-medium text-neutral-800 dark:text-neutral-200 flex items-center">
                            R-Factor
                            <TooltipProvider>
                                <Tooltip>
                                    <TooltipTrigger asChild>
                                        <button className="ml-2 text-neutral-500 hover:text-neutral-700 dark:text-neutral-400 dark:hover:text-neutral-200">
                                            <Info className="h-4 w-4" />
                                        </button>
                                    </TooltipTrigger>
                                    <TooltipContent className="max-w-xs">
                                        <p>Set the r-factor for the coloring algorithm (1 to k-1)</p>
                                    </TooltipContent>
                                </Tooltip>
                            </TooltipProvider>
                        </label>
                        <div className="relative">
                            <input
                                id="r-factor"
                                type="number"
                                min="1"
                                max={kColors - 1}
                                value={rFactor}
                                onChange={handleRFactorChange}
                                className="w-24 px-3 py-1.5 border border-neutral-300 dark:border-neutral-600 rounded-md text-right font-mono text-sm bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 focus:ring-2 focus:ring-neutral-500 focus:border-transparent transition-all"
                            />
                            <span className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-500 dark:text-neutral-400 text-sm pointer-events-none">
                                {rFactor}
                            </span>
                        </div>
                    </div>
                    <div className="flex justify-between text-xs text-neutral-500 dark:text-neutral-400 px-1">
                        <span>1</span>
                        <span>{kColors - 1}</span>
                    </div>
                    <input
                        type="range"
                        min="1"
                        max={kColors - 1}
                        value={rFactor}
                        onChange={handleRFactorChange}
                        className="w-full h-2 bg-neutral-200 dark:bg-neutral-700 rounded-full appearance-none cursor-pointer accent-neutral-900 dark:accent-neutral-200"
                    />
                </div>
            </div>
        </div>
    );
}