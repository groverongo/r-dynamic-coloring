import { useEffect, useImperativeHandle, useState } from "react";
import { Line } from "react-konva";
import EdgeProps from "./props";

export default function Edge({
    fromId,
    toId,
    from,
    to,
    ref,
    onSelect,
    compromised,
    theme
}: EdgeProps) {

    const [isSelected, setIsSelected] = useState<boolean>(false);
    const borderColor = theme === "light" ? "black" : "white";

    useImperativeHandle(ref, () => ({
        fromId: fromId,
        toId: toId,
        isSelected: isSelected,
        select: () => setIsSelected(true),
        deselect: () => setIsSelected(false),
    }));

    useEffect(() => {
        if (isSelected) {
            onSelect?.();
        }
    }, [isSelected]);

    return (
        <Line
            points={[from.x, from.y, to.x, to.y]}
            stroke={isSelected ? "blue" : borderColor}
            dash={compromised ? [7, 10] : []}
            strokeWidth={2}
            hitStrokeWidth={40}
            onClick={() => {
                setIsSelected(!isSelected);
            }}
        />
    );
}

