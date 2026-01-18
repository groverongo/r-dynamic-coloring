import { Canvg } from "canvg";
import Konva from "konva";
import {
  useEffect,
  useImperativeHandle,
  useRef,
  useState
} from "react";
import { Circle, Group, Image, Text } from "react-konva";
import { parse, stringify } from "svgson";
import TeXToSVG from "tex-to-svg";
import {
  VERTEX_COLORS,
  VERTEX_MODES,
  VERTEX_MODES_STYLE,
} from "../constant";
import { VertexProps } from "./props";
import { VertexRef } from "./ref";

export function Vertex({
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
  fontSize,
  nodeRadius,
  onDragEnd
}: Readonly<VertexProps>) {

  const [latex, setLatex] = useState<HTMLImageElement | undefined>();
  const [isSelected, setIsSelected] = useState<boolean>(false);
  const [text, setText] = useState<string>("");
  const RES_FACTOR = 50;
  const textColor = theme === "light" ? "black" : "white";
  const backgroundColor = theme === "light" ? "white" : "black";
  const borderColor = theme === "light" ? "black" : "white";

  const [colorIndex, setColorIndex] = useState<number | null>(
    colorIndexInitial
  );

  const extractDimensionEx = (attribute: string) => parseFloat(attribute.slice(0, attribute.length - 2));
  const redfineDimensionEx = (value: number) => (RES_FACTOR * value).toString() + "ex";


  useEffect(() => {
    const renderSvgToImage = async () => {
      const canvas = document.createElement("canvas");

      const textToRender = mode === 0 ? text : colorIndex?.toString() || "";

      let svgStr = TeXToSVG(textToRender, {
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
        if (v.name !== "g") return;
        v.attributes.fill = textColor;
      })

      svgStr = stringify(parsedSVG)

      const v = Canvg.fromString(canvas.getContext("2d")!, svgStr);

      await v.render()

      const dataUrl = canvas.toDataURL();

      const img = new window.Image(fontSize * equationDims.width / equationDims.height, fontSize);
      img.onload = () => {
        setLatex(img);
      };
      img.src = dataUrl;
    };

    renderSvgToImage();

    return () => {
      setLatex(undefined);
    };
  }, [text, colorIndex, mode, fontSize, theme]);

  const [neighbors, setNeighbors] = useState<VertexRef[]>([]);

  const GroupRef = useRef<Konva.Group>(null);

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
    addNeighbor: (neighbor: VertexRef) => {
      setNeighbors((prev) => [...prev, neighbor]);
    },
    removeNeighbor: (neighbor: VertexRef) => {
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
    changeColor: (index: number | null, enforce: boolean = false) => {
      if (!isSelected && !enforce) return;
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
      onDragEnd={(e) => {
        onDragEnd?.(getAbsoluteX(), getAbsoluteY());
      }}
    >
      <Circle
        x={x}
        y={y}
        radius={nodeRadius}
        fill={colorIndex === null ? backgroundColor : VERTEX_COLORS[colorIndex].hex}
        stroke={
          isSelected
            ? VERTEX_MODES_STYLE[VERTEX_MODES[mode]].strokeColor
            : borderColor
        }
        dash={compromised ? [5, 5] : []}
      />
      {latex && (
        <Image
          image={latex}
          x={x - latex.width / 2}
          y={y - latex.height / 2}
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
