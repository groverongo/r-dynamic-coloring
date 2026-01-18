type EdgeRef = {
    fromId: string;
    toId: string;
    isSelected: boolean;
    select: () => void;
    deselect: () => void;
    updatePosition: (from: { x: number; y: number }, to: { x: number; y: number }) => void;
}

export { EdgeRef };
