
import { Ref, useEffect, useImperativeHandle, useState } from "react";
import { Line } from "react-konva";

export type LinkGRef = {
    fromId: string;
    toId: string;
    isSelected: boolean;
    select: () => void;
    deselect: () => void;
}

type LinkGProps = {
    fromId: string;
    toId: string;
    from: {x: number, y: number};
    to: {x: number, y: number};
    ref?: Ref<LinkGRef>;
    onSelect?: () => void;
    compromised?: boolean;
}

export default function LinkG({
    fromId,
    toId,
    from,
    to,
    ref,
    onSelect,
    compromised,
}: LinkGProps) {

    const [isSelected, setIsSelected] = useState<boolean>(false);


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
            stroke={isSelected ? "blue" : "white"}
            dash={compromised ? [7, 10] : []}
            strokeWidth={2}
            hitStrokeWidth={40}
            onClick={() => {
                setIsSelected(!isSelected);
            }}
        />
    );
}

