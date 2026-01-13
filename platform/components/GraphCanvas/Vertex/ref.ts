type VertexRef = {
  x: number;
  y: number;
  text: string;
  colorIndex: number | null;
  isSelected: boolean;
  neighbors: VertexRef[];
  addNeighbor: (neighbor: VertexRef) => void;
  removeNeighbor: (neighbor: VertexRef) => void;
  select: () => void;
  deselect: () => void;
  appendCharacter: (character: string) => void;
  deleteCharacter: () => void;
  changeColor: (index: number | null, enforce?: boolean) => void;
};

export default VertexRef;