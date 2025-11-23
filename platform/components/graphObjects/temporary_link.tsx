import { Line } from "react-konva";

export default function TemporaryLinkG({
    from,
    to,
}: {
    from: {x: number, y: number};
    to: {x: number, y: number};
}) {
    return (
        <Line
            points={[from.x, from.y, to.x, to.y]}
            stroke="white"
            strokeWidth={2}
        />
    );
}

