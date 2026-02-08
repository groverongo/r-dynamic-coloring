import { MainCanvasContext } from "@/lib/graph-constants";
import { useGraphCanvasContext } from "@r-dynamic-coloring/graph-canvas";
import { SlidersVertical } from "lucide-react";

export function ElementProperties() {
    const {
        edgeCurrentId, vertexCurrentId
    } = useGraphCanvasContext(MainCanvasContext);

    return (
        <div className="bg-neutral-50 dark:bg-neutral-900 rounded-lg shadow-sm border border-neutral-200 dark:border-neutral-800 p-4 w-full max-w-md">
            <h3 className="text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-4 flex items-center">
                <span className="bg-neutral-100 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 border border-neutral-300 dark:border-neutral-600 rounded-full w-8 h-8 flex items-center justify-center mr-3 text-sm font-mono"><SlidersVertical /></span>
                Selected Element
            </h3>

            {edgeCurrentId && (
                <div className="text-sm font-medium text-neutral-800 dark:text-neutral-200 flex items-center">
                    <p>Selected element:</p>
                    <p> {edgeCurrentId}</p>
                </div>
            )}
            {vertexCurrentId && (
                <div className="text-sm font-medium text-neutral-800 dark:text-neutral-200 flex items-center">
                    <p>Selected element:</p>
                    <p> {vertexCurrentId}</p>
                </div>
            )}
            {edgeCurrentId && (
                <div className="text-sm font-medium text-neutral-800 dark:text-neutral-200 flex items-center">
                    <p>Selected element type:</p>
                    <p> Edge</p>
                </div>
            )}
            {vertexCurrentId && (
                <div className="text-sm font-medium text-neutral-800 dark:text-neutral-200 flex items-center">
                    <p>Selected element type:</p>
                    <p> Vertex</p>
                </div>
            )}
        </div>
    );
}