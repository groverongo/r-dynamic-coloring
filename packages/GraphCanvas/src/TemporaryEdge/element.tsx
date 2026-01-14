import { Line } from "react-konva";
import { TemporaryLinkGProps } from "./props";

export function TemporaryLinkG({
    from,
    to,
    theme
}: TemporaryLinkGProps) {
    return (
        <Line
            points={[from.x, from.y, to.x, to.y]}
            stroke={theme == 'dark' ? "white" : "black"}
            strokeWidth={2}
        />
    );
}

