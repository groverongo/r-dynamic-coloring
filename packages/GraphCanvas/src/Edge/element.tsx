import Konva from "konva";
import { useEffect, useImperativeHandle, useRef, useState } from "react";
import { Line } from "react-konva";
import { EdgeProps } from "./props";

export function Edge({
    fromId,
    toId,
    from,
    to,
    ref,
    onSelect,
    onDeselect,
    compromised,
    theme
}: EdgeProps) {

    const [isSelected, setIsSelected] = useState<boolean>(false);
    const borderColor = theme === "light" ? "black" : "white";

    const lineRef = useRef<Konva.Line>(null);

    useImperativeHandle(ref, () => ({
        fromId: fromId,
        toId: toId,
        isSelected: isSelected,
        select: () => setIsSelected(true),
        deselect: () => setIsSelected(false),
        updatePosition: (newFrom: { x: number, y: number }, newTo: { x: number, y: number }) => {
            if (lineRef.current) {
                lineRef.current.points([newFrom.x, newFrom.y, newTo.x, newTo.y]);
                lineRef.current.getLayer()?.batchDraw();
            }
        }
    }), [fromId, toId, isSelected, from.x, from.y, to.x, to.y]);

    useEffect(() => {
        if (isSelected) {
            onSelect?.();
        }
    }, [isSelected]);

    return (
        <Line
            ref={lineRef}
            points={[from.x, from.y, to.x, to.y]}
            stroke={isSelected ? "blue" : borderColor}
            dash={compromised ? [7, 10] : []}
            strokeWidth={2}
            hitStrokeWidth={40}
            onClick={() => {
                setIsSelected(prev => {
                    if (prev) {
                        onDeselect?.();
                    }
                    return !prev;
                });
            }}
        />
    );
}

