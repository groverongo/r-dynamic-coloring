import Konva from "konva";
import {
  FocusEventHandler,
  KeyboardEventHandler,
  LegacyRef,
  useEffect, useMemo, useRef, useState
} from "react";
import { Image, Layer, Stage } from "react-konva";
import { v4 as uuidv4 } from 'uuid';
import { useGraphCanvasContext } from "../Context/useContext";
import { Edge } from "../Edge/element";
import { TemporaryLinkG } from "../TemporaryEdge/element";
import { Vertex } from "../Vertex/element";
import { VERTEX_MODES, isIntString } from "../constant";
import { GraphCanvasProps } from "./props";

export function GraphCanvas({ styleProps, context, fontSize, nodeRadius, theme, triggers }: GraphCanvasProps) {

  const {
    vertexGraph, setVertexGraph,
    edgeGraph, setEdgeGraph,
    graphAdjacencyList, setGraphAdjacencyList,
    coloring, setColoring,
    rFactor,
    kColors,
    vertexCurrentId, setVertexCurrentId,
    edgeCurrentId, setEdgeCurrentId,
    stageRef,
    vertexRefs,
    edgeRefs
  } = useGraphCanvasContext(context);

  const [nodeMode, setNodeMode] = useState<number>(0);

  const [closestVertexId, setClosestVertexId] = useState<string | null>(null);
  const [keyDownUnblock, setKeyDownUnblock] = useState<boolean>(true);

  const [compromisedVertices, setCompromisedVertices] = useState<Set<string>>(new Set<string>());
  const [compromisedEdges, setCompromisedEdges] = useState<Set<string>>(new Set<string>());

  const [shiftPressed, setShiftPressed] = useState<boolean>(false);
  const [mouseDownPos, setMouseDownPos] = useState<{
    x: number;
    y: number;
  } | null>(null);

  const onBlur: FocusEventHandler<HTMLDivElement> = (e) => {
    setKeyDownUnblock(true);
    setShiftPressed(false);
  };

  const onKeyUp: KeyboardEventHandler<HTMLDivElement> = (e) => {
    setKeyDownUnblock(true);
    if (e.key === "Shift") setShiftPressed(false);
  };

  const onKeyDown: KeyboardEventHandler<HTMLDivElement> = (e) => {
    if (keyDownUnblock) setKeyDownUnblock(false);

    if (e.key === "Shift") {
      setShiftPressed(true);
    }

    if (vertexCurrentId !== null) {
      const ref = vertexRefs.current?.get(vertexCurrentId);

      if (ref === null || ref === undefined) return;

      if (e.key.length === 1 && /^[a-zA-Z0-9_\\^{}]$/.test(e.key)) {
        if (VERTEX_MODES[nodeMode] === "Label") {
          ref.appendCharacter(e.key);
        } else if (VERTEX_MODES[nodeMode] === "Color" && isIntString(e.key)) {
          if (+e.key >= kColors) return;
          ref.changeColor(+e.key === coloring[vertexCurrentId] ? null : +e.key);
          setColoring((prev) => {
            const newColoring = { ...prev };
            if (newColoring[vertexCurrentId] === +e.key) {
              delete newColoring[vertexCurrentId];
            } else {
              newColoring[vertexCurrentId] = +e.key;
            }
            return newColoring;
          });
        }
      } else if (e.key === "Backspace") {
        if (VERTEX_MODES[nodeMode] === "Label") {
          ref.deleteCharacter();
        } else if (VERTEX_MODES[nodeMode] === "Color") {
          ref.changeColor(null);
        }
      } else if (e.key === "Delete") {
        ref.deselect();

        const edgeTuples = graphAdjacencyList.get(vertexCurrentId);

        setGraphAdjacencyList((prev) => {
          const newMap = new Map(prev);

          edgeTuples?.forEach((edgeTuple) => {
            const edge = edgeGraph.get(edgeTuple[1]);
            if (edge === undefined) return;
            newMap.get(edgeTuple[0])?.delete(edge.fromEntry);
          });
          newMap.delete(vertexCurrentId);

          return newMap;
        });
        setEdgeGraph((prev) => {
          const newMap = new Map(prev);
          edgeTuples?.forEach((edgeTuple) => {
            newMap.delete(edgeTuple[1]);
          });
          return newMap;
        });
        setVertexGraph((prev) => {
          const newMap = new Map(prev);
          newMap.delete(vertexCurrentId);
          return newMap;
        });
        setVertexCurrentId(null);
      } else if (e.key === "Control") {
        setNodeMode((prev) => (prev + 1) % VERTEX_MODES.length);
      }
    } else if (edgeCurrentId !== null) {
      const ref = edgeRefs.current?.get(edgeCurrentId);

      if (ref === null || ref === undefined) return;

      if (e.key === "Delete") {
        ref.deselect();
        setGraphAdjacencyList((prev) => {
          const edge = edgeGraph.get(edgeCurrentId);
          if (edge === undefined) return prev;
          const newMap = new Map(prev);
          newMap.get(edge.from)?.delete(edge.toEntry);
          newMap.get(edge.to)?.delete(edge.fromEntry);
          return newMap;
        });
        setEdgeGraph((prev) => {
          const newMap = new Map(prev);
          newMap.delete(edgeCurrentId);
          return newMap;
        });
        setEdgeCurrentId(null);
      }
    }
  };

  function deselectObjects(vertexId: string | null, edgeId: string | null) {
    if (vertexCurrentId !== null && vertexCurrentId !== vertexId) {
      vertexRefs.current?.get(vertexCurrentId)?.deselect();
    }
    setVertexCurrentId(vertexId);

    if (edgeCurrentId !== null && edgeCurrentId !== edgeId) {
      edgeRefs.current?.get(edgeCurrentId)?.deselect();
    }
    setEdgeCurrentId(edgeId);
  }

  useEffect(() => {

    const compromisedVerticesLocal: Set<string> = new Set<string>();
    const compromisedEdgesLocal: Set<string> = new Set<string>();

    for (const [vertex, edges] of graphAdjacencyList) {
      const sourceVertexColor = coloring[vertex];
      const neighborColors = new Set<number>();
      for (const [neighborVertex, edgeId] of edges) {
        neighborColors.add(coloring[neighborVertex]);
        if (coloring[neighborVertex] === sourceVertexColor) {
          compromisedEdgesLocal.add(edgeId);
        }
      }

      if (neighborColors.size < Math.min(rFactor, edges.size)) {
        compromisedVerticesLocal.add(vertex);
      }
    }

    setCompromisedVertices(compromisedVerticesLocal);
    setCompromisedEdges(compromisedEdgesLocal);
  }, [coloring]);

  useEffect(() => {
    vertexRefs.current?.clear();
    for (const id of vertexGraph.keys()) {
      vertexRefs.current?.set(id, vertexRefs.current?.get(id) ?? null);
    }

    if (vertexCurrentId !== null) {
      vertexRefs.current?.get(vertexCurrentId)?.deselect();

      const [_, ref] = Array.from(vertexRefs?.current ?? [null, null]).at(-1) ?? [null, null];
      ref?.select();
    }
  }, [vertexGraph.size]);

  useEffect(() => {
    edgeRefs.current?.clear();
    for (const id of edgeGraph.keys()) {
      edgeRefs.current?.set(id, edgeRefs.current?.get(id) ?? null);
    }

    if (edgeCurrentId !== null) {
      edgeRefs.current?.get(edgeCurrentId)?.deselect();
      const [_, ref] = Array.from(edgeRefs?.current ?? [null, null]).at(-1) ?? [null, null];
      ref?.select();
    }
  }, [edgeGraph.size]);

  const drawingImageRef = useRef<Konva.Image>(null);

  const { drawingCanvas, drawingContext } = useMemo(() => {
    const canvas = document.createElement('canvas');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight - 25;
    const context = canvas.getContext('2d');
    if (context === null) return { drawingCanvas: undefined, drawingContext: undefined };
    context.strokeStyle = theme === 'dark' ? '#ffffff' : '#000000';
    context.lineJoin = 'round';
    context.lineWidth = 5;
    return { drawingCanvas: canvas, drawingContext: context };
  }, [theme]);

  return (
    <div onKeyDown={onKeyDown} onKeyUp={onKeyUp} onBlur={onBlur} tabIndex={0}>
      <Stage
        id="KonvaStage"
        className="bg-zinc-100 dark:bg-zinc-900"
        style={styleProps}
        width={styleProps.width as number}
        height={styleProps.height as number}
        ref={stageRef as LegacyRef<Konva.Stage>}
        onDblClick={(e) => {
          if (!keyDownUnblock) return;

          const vertexId = uuidv4();
          setGraphAdjacencyList((prev) => {
            const newMap = new Map(prev);
            newMap.set(vertexId, new Set<[string, string]>());
            return newMap;
          });
          setVertexGraph((prev) => {
            const newMap = new Map(prev);
            newMap.set(vertexId, { x: e.evt.offsetX, y: e.evt.offsetY, xRelative: e.evt.offsetX, yRelative: e.evt.offsetY });
            return newMap;
          });
        }}
        onMouseMove={(e) => {
          if (mouseDownPos === null) return;
          if (shiftPressed) {
            for (const [i, ref] of vertexRefs.current?.entries() ?? []) {
              if (ref === null) continue;

              const distance = Math.sqrt(
                Math.pow(ref.x - e.evt.offsetX, 2) +
                Math.pow(ref.y - e.evt.offsetY, 2)
              );
              if (distance > 60) continue;
              setClosestVertexId(i);
              setMouseDownPos({ x: ref.x, y: ref.y });
              return;
            }
            setClosestVertexId(null);
            setMouseDownPos({ x: e.evt.offsetX, y: e.evt.offsetY });
          } else if (vertexCurrentId === null) {
            const image = drawingImageRef.current;

            drawingContext?.beginPath();
            drawingContext?.moveTo(mouseDownPos.x, mouseDownPos.y);
            drawingContext?.lineTo(e.evt.offsetX, e.evt.offsetY);
            drawingContext?.closePath();
            drawingContext?.stroke();
            setMouseDownPos({ x: e.evt.offsetX, y: e.evt.offsetY });
            if (image === null) return;
            image.getLayer()?.batchDraw();
          }
        }}
        onMouseDown={(e) => {
          setMouseDownPos({ x: e.evt.offsetX, y: e.evt.offsetY });
        }}
        onMouseUp={(e) => {
          if (mouseDownPos === null || !shiftPressed) {
            setMouseDownPos(null);
            return;
          }
          if (closestVertexId !== null && vertexCurrentId !== null && vertexCurrentId !== closestVertexId) {
            const edgeId = uuidv4();
            const fromEntry: [string, string] = [vertexCurrentId, edgeId];
            const toEntry: [string, string] = [closestVertexId, edgeId];
            const vertexAdjacentSet = graphAdjacencyList.get(vertexCurrentId);
            if (vertexAdjacentSet !== undefined) {
              for (const [vertexId, _] of vertexAdjacentSet) {
                if (vertexId === closestVertexId) {
                  triggers?.existingEdge?.(vertexCurrentId, closestVertexId);
                  setMouseDownPos(null);
                  return;
                }
              }
            }

            setEdgeGraph((prev) => {
              const newMap = new Map(prev);
              newMap.set(edgeId, { from: vertexCurrentId, to: closestVertexId, fromEntry, toEntry });
              return newMap;
            });
            setGraphAdjacencyList((prev) => {
              const newMap = new Map(prev);
              newMap.get(vertexCurrentId)?.add(toEntry);
              newMap.get(closestVertexId)?.add(fromEntry);
              return newMap;
            });
            setClosestVertexId(null);
          }
          setMouseDownPos(null);
        }}
      >
        <Layer />
        <Layer>
          <Image
            ref={drawingImageRef}
            image={drawingCanvas}
            x={0}
            y={0}
          />
          {shiftPressed &&
            mouseDownPos !== null &&
            vertexCurrentId !== null && (
              <TemporaryLinkG
                from={{
                  x: vertexRefs.current?.get(vertexCurrentId)?.x || 0,
                  y: vertexRefs.current?.get(vertexCurrentId)?.y || 0,
                }}
                to={{ x: mouseDownPos.x, y: mouseDownPos.y }}
                theme={theme as 'light' | 'dark'}
              />
            )}
          {Array.from(edgeGraph.entries()).map(([index, edge]) => {

            const fromRef = vertexGraph.get(edge.from);
            const toRef = vertexGraph.get(edge.to);

            const from = fromRef ? { x: fromRef.xRelative, y: fromRef.yRelative } : { x: 0, y: 0 };
            const to = toRef ? { x: toRef.xRelative, y: toRef.yRelative } : { x: 0, y: 0 };

            return (<Edge
              key={index}
              ref={(e) => {
                edgeRefs.current?.set(index, e);
              }}
              compromised={compromisedEdges.has(index)}
              onSelect={() => {
                deselectObjects(null, index);
              }}
              onDeselect={() => {
                setEdgeCurrentId(null);
                edgeRefs.current?.get(index)?.deselect();
              }}
              fromId={edge.from}
              toId={edge.to}
              theme={theme as 'light' | 'dark'}
              from={from}
              to={to}
            />)
          })}
          {Array.from(graphAdjacencyList.keys()).map((key) => {

            const allowedColors = new Set(Array.from({ length: kColors }, (_, i) => i));
            allowedColors.delete(coloring[key]);
            for (const [vertex, _] of graphAdjacencyList.get(key) ?? []) {
              allowedColors.delete(coloring[vertex]);
            }

            return (<Vertex
              key={key}
              fontSize={fontSize}
              nodeRadius={nodeRadius}
              ref={(e) => {
                vertexRefs.current?.set(key, e);
              }}
              theme={theme as 'light' | 'dark'}
              colorIndexInitial={coloring[key] ?? null}
              x={vertexGraph.get(key)?.x || 0}
              y={vertexGraph.get(key)?.y || 0}
              onSelect={() => {
                deselectObjects(key, null);
              }}
              onDeselect={() => {
                setVertexCurrentId(null);
                vertexRefs.current?.get(key)?.deselect();
              }}
              allowedColors={allowedColors}
              compromised={compromisedVertices.has(key)}
              draggable={keyDownUnblock}
              mode={nodeMode}
              whileDragging={(x, y) => {
                // Update connected edges directly
                const edges = graphAdjacencyList.get(key);
                if (edges) {
                  edges.forEach((edgeTuple) => {
                    const edgeId = edgeTuple[1];
                    const edgeRef = edgeRefs.current?.get(edgeId);
                    const neighborId = edgeTuple[0];
                    const neighborNode = vertexGraph.get(neighborId);

                    if (edgeRef && neighborNode) {
                      const edgeData = edgeGraph.get(edgeId);
                      if (edgeData) {
                        // Determine if we are updating 'from' or 'to'
                        // The edgeData has from/to. 
                        // If key === edgeData.from, then we updated 'from'.

                        const isFrom = key === edgeData.from;

                        const newFrom = isFrom
                          ? { x: x, y: y }
                          : { x: neighborNode.xRelative, y: neighborNode.yRelative };

                        const newTo = isFrom
                          ? { x: neighborNode.xRelative, y: neighborNode.yRelative }
                          : { x: x, y: y };

                        edgeRef.updatePosition(newFrom, newTo);
                      }
                    }
                  });
                }
              }}
              onDragEnd={(x, y) => {
                setVertexGraph((prev) => {
                  const newMap = new Map(prev);
                  const current = newMap.get(key);
                  if (current === undefined) return newMap;

                  newMap.set(key, { ...current, xRelative: x, yRelative: y });
                  return newMap;
                });
              }}
            />)
          })}
        </Layer>
      </Stage>
    </div>
  );
}
