import { fontSizeAtom, nodeRadiusAtom } from "@/lib/atoms";
import {
  NODE_G_COLORS,
  NODE_G_MODES,
  NODE_G_MODES_STYLE,
} from "@/lib/graph-constants";
import { useAtomValue } from "jotai";
import Konva from "konva";
import { Ref, useEffect, useImperativeHandle, useRef, useState } from "react";
import { Circle, Group, Text } from "react-konva";

export type NodeGRef = {
  x: number;
  y: number;
  text: string;
  colorIndex: number | null;
  isSelected: boolean;
  neighbors: NodeGRef[];
  addNeighbor: (neighbor: NodeGRef) => void;
  removeNeighbor: (neighbor: NodeGRef) => void;
  select: () => void;
  deselect: () => void;
  appendCharacter: (character: string) => void;
  deleteCharacter: () => void;
  changeColor: (index: number | null) => void;
};

export type NodeGProps = {
  ref?: Ref<NodeGRef>;
  colorIndexInitial: number | null;
  x: number;
  y: number;
  onSelect?: () => void;
  draggable?: boolean;
  mode: number;
  compromised?: boolean;
  whileDragging?: (x: number, y: number) => void;
  allowedColors?: Set<number>;
};

export default function NodeG({
  ref,
  x,
  y,
  onSelect,
  draggable,
  mode,
  whileDragging,
  compromised,
  allowedColors,
  colorIndexInitial
}: Readonly<NodeGProps>) {
  const [isSelected, setIsSelected] = useState<boolean>(false);
  const [text, setText] = useState<string>("");

  const [neighbors, setNeighbors] = useState<NodeGRef[]>([]);

  const GroupRef = useRef<Konva.Group>(null);

  const [colorIndex, setColorIndex] = useState<number | null>(colorIndexInitial);

  const nodeRadius = useAtomValue(nodeRadiusAtom);
  const fontSize = useAtomValue(fontSizeAtom);

  const getAbsoluteX = () => {
    return GroupRef.current ? GroupRef.current.x() + x : x;
  }

  const getAbsoluteY = () => {
    return GroupRef.current ? GroupRef.current.y() + y : y;
  }

  
  useImperativeHandle(ref, () => ({
    x: getAbsoluteX(),
    y: getAbsoluteY(),
    text: text,
    colorIndex: colorIndex,
    isSelected: isSelected,
    neighbors: neighbors,
    addNeighbor: (neighbor: NodeGRef) => {
      setNeighbors((prev) => [...prev, neighbor]);
    },
    removeNeighbor: (neighbor: NodeGRef) => {
      setNeighbors((prev) => prev.filter((n) => n !== neighbor));
    },
    select: () => {
      setIsSelected(true);
    },
    deselect: () => {
      setIsSelected(false);
    },
    appendCharacter: (character: string) => {
      setText((prev) => prev + character);
    },
    deleteCharacter: () => {
      if (text.length === 0) return;
      setText((prev) => prev.substring(0, prev.length - 1));
    },
    changeColor: (index: number | null) => {
      if (!isSelected) return;
      setColorIndex(index);
    },
  }));

  useEffect(() => {
    if (isSelected) {
      onSelect?.();
    }
  }, [isSelected]);

  return (
      <Group
        ref={GroupRef}
        onClick={() => {
          setIsSelected(!isSelected);
        }}
        draggable={draggable}
        onDragStart={() => {
          setIsSelected(true);
        }}
        onDragMove={(e) => {
          whileDragging?.(getAbsoluteX(), getAbsoluteY());
        }}
      >
        <Circle
          x={x}
          y={y}
          radius={nodeRadius}
          fill={colorIndex === null ? "black" : NODE_G_COLORS[colorIndex].hex}
          stroke={
            isSelected
              ? NODE_G_MODES_STYLE[NODE_G_MODES[mode]].strokeColor
              : "white"
          }
          dash={compromised ? [5, 5] : []}
        />
        <Text
          text={mode === 0 ? text : colorIndex?.toString()}
          x={x - 5 * (mode === 0 ? text.length : colorIndex?.toString().length || 0)}
          y={y - 10}
          fontSize={fontSize}
          fill="white"
        />
      { mode === 1 &&
        Array.from(allowedColors?.values() ?? []).map((color, index, colors) => {
          return (
            <Text
              key={index}
              text={color.toString()}
              x={x + nodeRadius - 15 * (colors.length - index)}
              y={y + nodeRadius + 5}
              fontSize={fontSize / 1.3 }
              fill="white"

            />
          );
        })
      }
    </Group>
  );
}
