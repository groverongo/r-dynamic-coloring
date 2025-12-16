import { Line } from "react-konva";

type TemporaryLinkGProps = {
    from: {x: number, y: number};
    to: {x: number, y: number};
    theme: 'light' | 'dark';
}

export default function TemporaryLinkG({
    from,
    to,
    theme
}: TemporaryLinkGProps) {
    return (
        <Line
            points={[from.x, from.y, to.x, to.y]}
            stroke= {theme == 'dark' ? "white": "black"}
            strokeWidth={2}
        />
    );
}

