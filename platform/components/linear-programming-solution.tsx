import { Cpu, Info, Send } from "lucide-react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "./ui/tooltip";
import { useState } from "react";
import { Button } from "./ui/button";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { useAtomValue, useSetAtom } from "jotai";
import { coloringAtom, graphAdjacencyListAtom, kColorsAtom, rFactorAtom } from "@/lib/atoms";
import z from "zod";
import { GraphSerializer } from "@/lib/serializers";
import { useElementRef } from "@/lib/refs";

export function LPSolution() {
    const graphAdjacencyList = useAtomValue(graphAdjacencyListAtom);
    const setKColors = useSetAtom(kColorsAtom);
    const setRFactor = useSetAtom(rFactorAtom);
    const setColoring = useSetAtom(coloringAtom);

    const { vertexRefs } = useElementRef();


    const [kColorsLocal, setKColorsLocal] = useState(2);
    const [rFactorLocal, setRFactorLocal] = useState(1);
    const [lpMethod, setLPMethod] = useState<"ACR" | "ACR_H" | "ACR_R" | "ACR_RH">("ACR");

    const { isSuccess, error, mutateAsync, isPending } = useMutation({
        mutationFn: async () => {
            const responseSchema = z.object({
                coloring: z.record(z.string(), z.number()),
            });

            const response = await axios.post(`${process.env.NEXT_PUBLIC_R_HUED_COLORING_API}/coloring/linear-program`, {
                graph: JSON.parse(GraphSerializer.simpleGraphAdjacencyListSerializer(graphAdjacencyList)),
                k: kColorsLocal,
                r: rFactorLocal,
                method: lpMethod,
            });

            const data = responseSchema.parse(response.data);
            return data;
        },
        retry: false
    });

    const handleSubmit = () => {
        if (graphAdjacencyList.size === 0) return;
        setKColors(kColorsLocal);
        setRFactor(rFactorLocal);
        mutateAsync().then(data => {
            const refs = vertexRefs.current;
            if (refs === null) return;
            Object.entries(data.coloring).forEach(([vertex, color]) => {
                const ref = refs.get(vertex);
                if (ref === null || ref === undefined) return;
                ref.changeColor(color, true);
            });
            setColoring(data.coloring);
        }).catch(error => {
            console.error('Error:', error);
        });
    };

    const handleRFactorChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = Number.parseInt(e.target.value, 10);
        if (!Number.isNaN(value) && value >= 1) {
            setRFactorLocal(value);
        }
    };

    const handleKColorsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = Number.parseInt(e.target.value, 10);
        if (!Number.isNaN(value) && value >= 2) {
            setKColorsLocal(value);
        }
    };

    const handleLPMethodChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setLPMethod(e.target.value as "ACR" | "ACR_H" | "ACR_R" | "ACR_RH");
    };

    return (
        <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg shadow-sm border border-neutral-200 dark:border-neutral-800 p-4 w-full max-w-md">
            <h3 className="text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-4 flex items-center">
                <span className="bg-neutral-100 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 border border-neutral-300 dark:border-neutral-600 rounded-full w-8 h-8 flex items-center justify-center mr-3 text-sm font-mono"><Cpu /></span>
                Apply LP  Coloring Model

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
                                value={kColorsLocal}
                                onChange={handleKColorsChange}
                                className="w-24 px-3 py-1.5 border border-neutral-300 dark:border-neutral-600 rounded-md text-right font-mono text-sm bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 focus:ring-2 focus:ring-neutral-500 focus:border-transparent transition-all"
                            />
                        </div>
                    </div>
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
                                max={kColorsLocal - 1}
                                value={rFactorLocal}
                                onChange={handleRFactorChange}
                                className="w-24 px-3 py-1.5 border border-neutral-300 dark:border-neutral-600 rounded-md text-right font-mono text-sm bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 focus:ring-2 focus:ring-neutral-500 focus:border-transparent transition-all"
                            />
                        </div>
                    </div>
                </div>

                <div className="space-y-1">
                    <div className="flex items-center justify-between">
                        <label htmlFor="lp-method" className="text-sm font-medium text-neutral-800 dark:text-neutral-200 flex items-center">
                            LP Method
                            <TooltipProvider>
                                <Tooltip>
                                    <TooltipTrigger asChild>
                                        <button className="ml-2 text-neutral-500 hover:text-neutral-700 dark:text-neutral-400 dark:hover:text-neutral-200">
                                            <Info className="h-4 w-4" />
                                        </button>
                                    </TooltipTrigger>
                                    <TooltipContent className="max-w-xs">
                                        <p>Set the LP method to use for the coloring algorithm</p>
                                        <ul>
                                            <li>ACR: Solve using standard r-dynamic coloring constraints</li>
                                            <li>ACR-H: Solve using standard r-dynamic coloring constraints with a heuristic</li>
                                            <li>ACR-R: Solve using standard r-dynamic coloring constraints using a previous solution as a starting point</li>
                                            <li>ACR-RH: Solve using standard r-dynamic coloring constraints using a previous solution as a starting point and a heuristic</li>
                                        </ul>
                                    </TooltipContent>
                                </Tooltip>
                            </TooltipProvider>
                        </label>
                        <div className="relative">
                            <select
                                id="lp-method"
                                value={lpMethod}
                                onChange={handleLPMethodChange}
                                className="w-24 px-3 py-1.5 border border-neutral-300 dark:border-neutral-600 rounded-md text-right font-mono text-sm bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 focus:ring-2 focus:ring-neutral-500 focus:border-transparent transition-all"
                            >
                                <option value="ACR">ACR</option>
                                <option value="ACR_H">ACR-H</option>
                                <option value="ACR_R">ACR-R</option>
                                <option value="ACR_RH">ACR-RH</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div className="pt-4">
                    <Button
                        onClick={handleSubmit}
                        disabled={isPending}
                        className="w-full bg-neutral-900 hover:bg-neutral-800 text-white dark:bg-neutral-800 dark:hover:bg-neutral-700 transition-colors"
                    >
                        {isPending ? (
                            'Processing...'
                        ) : (
                            <>
                                <Send className="mr-2 h-4 w-4" />
                                Solve Linear Program
                            </>
                        )}
                    </Button>
                    {/* 
                    {response && (
                        <div className={`mt-4 p-3 rounded-md text-sm relative ${response.success
                            ? 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800'
                            : 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800'
                            }`}>
                            <button
                                onClick={() => setResponse(null)}
                                className="absolute top-2 right-2 text-neutral-400 hover:text-neutral-600 dark:text-neutral-400 dark:hover:text-neutral-200"
                                aria-label="Close message"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <line x1="18" y1="6" x2="6" y2="18"></line>
                                    <line x1="6" y1="6" x2="18" y2="18"></line>
                                </svg>
                            </button>
                            <div className="pr-4">
                                <p className="font-medium">
                                    {response.success ? 'Success!' : 'Error'}
                                </p>
                                <p className="mt-1">{response.message}</p>
                                {response.data && (
                                    <pre className="mt-2 p-2 bg-white/50 dark:bg-black/20 rounded overflow-auto text-xs">
                                        {JSON.stringify(response.data, null, 2)}
                                    </pre>
                                )}
                            </div>
                        </div>
                    )} */}
                </div>
            </div>
        </div>
    );
}