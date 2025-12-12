"use client"
import { fontSizeAtom, nodeRadiusAtom } from "@/lib/atoms";
import {
  NODE_G_COLORS,
  NODE_G_MODES,
  NODE_G_MODES_STYLE,
} from "@/lib/graph-constants";
import { useAtomValue } from "jotai";
import Konva from "konva";
import React, {
  Ref,
  useEffect,
  useImperativeHandle,
  useRef,
  useState,
} from "react";
import { Circle, Group, Text, Image } from "react-konva";
import { Canvg } from "canvg";
import TeXToSVG from "tex-to-svg";
import { parse, stringify } from "svgson";

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
  theme: 'light' | 'dark';
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
  colorIndexInitial,
  theme,
}: Readonly<NodeGProps>) {

  const [latex, setLatex] = useState<HTMLImageElement | undefined>();
  const [isSelected, setIsSelected] = useState<boolean>(false);
  const [text, setText] = useState<string>("");
  const RES_FACTOR = 50;
  const textColor = theme === "light" ? "black" : "white";
  const backgroundColor = theme === "light" ? "white" : "black";
  const borderColor = theme === "light" ? "black" : "white";

  const extractDimensionEx = (attribute: string) => parseFloat(attribute.slice(0, attribute.length-2));
  const redfineDimensionEx = (value: number) => (RES_FACTOR*value).toString() + "ex"; 

  useEffect(() => {
    const renderSvgToImage = async () => {
      const canvas = document.createElement("canvas");

      console.log(text)
      let svgStr = TeXToSVG(text, {
          ex: 10,
      });
      const parsedSVG = await parse(svgStr);
      const equationDims = {
        width: extractDimensionEx(parsedSVG.attributes.width), 
        height: extractDimensionEx(parsedSVG.attributes.height)
      };

      parsedSVG.attributes.fill = textColor;
      parsedSVG.attributes.height = redfineDimensionEx(equationDims.height);
      parsedSVG.attributes.width = redfineDimensionEx(equationDims.width);
      parsedSVG.children.forEach(v => {
        if(v.name !== "g") return;
        v.attributes.fill = textColor; 
      })

      console.log(parsedSVG)

      svgStr = stringify(parsedSVG)
      console.log(text, svgStr)

      const v = Canvg.fromString(canvas.getContext("2d")!, svgStr);

      await v.render()

      const dataUrl = canvas.toDataURL();

      const img = new window.Image(fontSize * equationDims.width/equationDims.height, fontSize);
      img.onload = () => {
        setLatex(img);
      };
      img.src = dataUrl;
    };

    renderSvgToImage();

    // Cleanup function (optional, but good practice for Konva Image assets)
    return () => {
      setLatex(undefined);
    };
  }, [text]);

  const [neighbors, setNeighbors] = useState<NodeGRef[]>([]);

  const GroupRef = useRef<Konva.Group>(null);

  const [colorIndex, setColorIndex] = useState<number | null>(
    colorIndexInitial
  );

  const nodeRadius = useAtomValue(nodeRadiusAtom);
  const fontSize = useAtomValue(fontSizeAtom);

  const getAbsoluteX = () => {
    return GroupRef.current ? GroupRef.current.x() + x : x;
  };

  const getAbsoluteY = () => {
    return GroupRef.current ? GroupRef.current.y() + y : y;
  };

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
        fill={colorIndex === null ? backgroundColor : NODE_G_COLORS[colorIndex].hex}
        stroke={
          isSelected
            ? NODE_G_MODES_STYLE[NODE_G_MODES[mode]].strokeColor
            : borderColor
        }
        dash={compromised ? [5, 5] : []}
      />
      {latex && (
        <Image
          image={latex}
          x={
            x -
            6.5 * (mode === 0 ? text.length : colorIndex?.toString().length || 0)
          }
          y={y - 8}
          // width={}
          height={fontSize}
        />
      )}
      {mode === 1 &&
        Array.from(allowedColors?.values() ?? []).map(
          (color, index, colors) => {
            return (
              <Text
                key={index}
                text={color.toString()}
                x={x + nodeRadius - 15 * (colors.length - index)}
                y={y + nodeRadius + 5}
                fontSize={fontSize / 1.3}
                fill={textColor}
              />
            );
          }
        )}
    </Group>
  );
}
