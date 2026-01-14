type EdgeRef = {
    fromId: string;
    toId: string;
    isSelected: boolean;
    select: () => void;
    deselect: () => void;
}

export { EdgeRef };
