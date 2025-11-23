import {
  CSSProperties,
  FocusEventHandler,
  KeyboardEventHandler,
  useEffect, useState
} from "react";
import { Layer, Rect, Stage } from "react-konva";
import NodeG, { NodeGRef } from "@/components/graphObjects/node";
import TemporaryLinkG from "@/components/graphObjects/temporary_link";
import LinkG, { LinkGRef } from "@/components/graphObjects/link";
import { NODE_G_MODES } from "@/lib/graph-constants";
import { isIntString } from "@/lib/utilities";
import { useAtom, useAtomValue, useSetAtom } from "jotai";
import { v4 as uuidv4 } from 'uuid';
import { coloringAtom, edgeCurrentIdAtom, edgeGraphAtom, graphAdjacencyListAtom, kColorsAtom, rFactorAtom, vertexCurrentIdAtom, vertexGraphAtom } from "@/lib/atoms";
import { useElementRef } from "@/lib/refs";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { GetGraphResponse } from "@/lib/validation";
import { GraphDeserializer } from "@/lib/serializers";

export default function Canvas({id}: {id?: string}) {
  const [styleProps, setStyleProps] = useState<CSSProperties>({});

  useEffect(() => {
    console.log(screen.width, screen.height)
    setStyleProps({
      height: screen.height / 1.6,
      width: (1200 * screen.width) / 2000,
      border: "3px solid white",
      borderRadius: "15px",
    });
  }, []);

  const {refetch, data} = useQuery({
    queryKey: ["graph", id],
    queryFn: async () => {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_R_HUED_COLORING_API}/graphs/${id}`)
      return response.data as GetGraphResponse;
    },
    retryOnMount: false,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    refetchOnReconnect: false,
  });

  const rFactor = useAtomValue(rFactorAtom);
  const kFactor = useAtomValue(kColorsAtom);

  const {vertexRefs, edgeRefs, stageRef} = useElementRef();

  const [vertexGraph, setVertexGraph] = useAtom(vertexGraphAtom);
  const [edgeGraph, setEdgeGraph] = useAtom(edgeGraphAtom);
  const [graphAdjacencyList, setGraphAdjacencyList] = useAtom(graphAdjacencyListAtom);

  const [nodeMode, setNodeMode] = useState<number>(0);
  const [vertexCurrentId, setVertexCurrentId] = useAtom(vertexCurrentIdAtom);
  const [edgeCurrentId, setEdgeCurrentId] = useAtom(edgeCurrentIdAtom);

  const [closestVertexId, setClosestVertexId] = useState<string | null>(null);
  const [keyDownUnblock, setKeyDownUnblock] = useState<boolean>(true);

  const [compromisedVertices, setCompromisedVertices] = useState<Set<string>>(new Set<string>());
  const [compromisedEdges, setCompromisedEdges] = useState<Set<string>>(new Set<string>());

  const [shiftPressed, setShiftPressed] = useState<boolean>(false);
  const [mouseDownPos, setMouseDownPos] = useState<{
    x: number;
    y: number;
  } | null>(null);

  const setKColors = useSetAtom(kColorsAtom);
  const setRFactor = useSetAtom(rFactorAtom);

  const [coloring, setColoring] = useAtom(coloringAtom);

  useEffect(() => {
    if (!id) return;
    refetch().then((response) => {
      if(response.data === undefined) return;

      
      
      setGraphAdjacencyList(GraphDeserializer.graphAdjacencyListDeserializer(response.data.graphAdjacencyList));
      setVertexGraph(GraphDeserializer.vertexGraphDeserializer(response.data.vertexGraph));
      setEdgeGraph(GraphDeserializer.edgeGraphDeserializer(response.data.edgeGraph));
      setColoring(GraphDeserializer.coloringDeserializer(response.data.localColoring));
      setKColors(response.data.localK);
      setRFactor(response.data.localR);
    });
  }, []);

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

      if (e.key.length === 1 && /^[a-zA-Z0-9]$/.test(e.key)) {
        if (NODE_G_MODES[nodeMode] === "Label") {
          ref.appendCharacter(e.key);
        } else if (NODE_G_MODES[nodeMode] === "Color" && isIntString(e.key)) {
          if(+e.key >= kFactor) return;
          ref.changeColor(+e.key === coloring[vertexCurrentId] ? null : +e.key);
          setColoring((prev) => {
            const newColoring = {...prev};
            if(newColoring[vertexCurrentId] === +e.key) {
              delete newColoring[vertexCurrentId];
            } else {
              newColoring[vertexCurrentId] = +e.key;
            }
            return newColoring;
          });
        }
      } else if (e.key === "Backspace") {
          if (NODE_G_MODES[nodeMode] === "Label") {
            ref.deleteCharacter();
          } else if (NODE_G_MODES[nodeMode] === "Color") {
            ref.changeColor(null);
          }
      } else if (e.key === "Delete") {
        ref.deselect();

        const edgeTuples = graphAdjacencyList.get(vertexCurrentId);

        setGraphAdjacencyList((prev) => {
          const newMap = new Map(prev);
          
          edgeTuples?.forEach((edgeTuple) => {
            const edge = edgeGraph.get(edgeTuple[1]);
            if(edge === undefined) return;
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
        setNodeMode((prev) => (prev + 1) % NODE_G_MODES.length);
      }
    } else if (edgeCurrentId !== null) {
      const ref = edgeRefs.current?.get(edgeCurrentId);

      if (ref === null || ref === undefined) return;

      if (e.key === "Delete") {
        ref.deselect();
        setGraphAdjacencyList((prev) => {
          const edge = edgeGraph.get(edgeCurrentId);
          if(edge === undefined) return prev;
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
        if(coloring[neighborVertex] === sourceVertexColor) {
          compromisedEdgesLocal.add(edgeId);
        }
      } 

      if(neighborColors.size < Math.min(rFactor, edges.size)) {
        compromisedVerticesLocal.add(vertex);
      }
    }

    console.log('compromisedVertices', compromisedVerticesLocal);
    console.log('compromisedEdges', compromisedEdgesLocal);
    
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

  useEffect(() => {
    console.log('graphAdjacencyList', graphAdjacencyList)
  }, [graphAdjacencyList])

  return (
    <div onKeyDown={onKeyDown} onKeyUp={onKeyUp} onBlur={onBlur} tabIndex={0}>
      <Stage
        id="KonvaStage"
        className="bg-zinc-100 dark:bg-zinc-900"
        style={styleProps}
        width={styleProps.width as number}
        height={styleProps.height as number}
        ref={stageRef}
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
            newMap.set(vertexId, {x: e.evt.offsetX, y: e.evt.offsetY, xRelative: e.evt.offsetX, yRelative: e.evt.offsetY});
            return newMap;
          });
        }}
        onMouseMove={(e) => {
          if (mouseDownPos === null) return;
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
        }}
        onMouseDown={(e) => {
          setMouseDownPos({ x: e.evt.offsetX, y: e.evt.offsetY });
        }}
        onMouseUp={(e) => {
          if (mouseDownPos === null) return;
          if (closestVertexId !== null && vertexCurrentId !== null && vertexCurrentId !== closestVertexId) {
            const edgeId = uuidv4();
            const fromEntry: [string, string] = [vertexCurrentId, edgeId];
            const toEntry: [string, string] = [closestVertexId, edgeId];
            setEdgeGraph((prev) => {
              const newMap = new Map(prev);
              newMap.set(edgeId, {from: vertexCurrentId, to: closestVertexId, fromEntry, toEntry});
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
        <Layer/>
        <Layer>
          {shiftPressed &&
            mouseDownPos !== null &&
            vertexCurrentId !== null && (
              <TemporaryLinkG
                from={{
                  x: vertexRefs.current?.get(vertexCurrentId)?.x || 0,
                  y: vertexRefs.current?.get(vertexCurrentId)?.y || 0,
                }}
                to={{ x: mouseDownPos.x, y: mouseDownPos.y }}
              />
            )}
          {Array.from(edgeGraph.entries()).map(([index, edge]) => {

            const fromRef = vertexGraph.get(edge.from);
            const toRef = vertexGraph.get(edge.to);

            const from = fromRef ? {x: fromRef.xRelative, y: fromRef.yRelative} : {x: 0, y: 0};
            const to = toRef ? {x: toRef.xRelative, y: toRef.yRelative} : {x: 0, y: 0};

            return (<LinkG
              key={index}
              ref={(e) => {
                edgeRefs.current?.set(index, e);
              }}
              compromised={compromisedEdges.has(index)}
              onSelect={() => {
                deselectObjects(null, index);
              }}
              fromId={edge.from}
              toId={edge.to}
              from={from}
              to={to}
            />)
          })}
          {Array.from(graphAdjacencyList.keys()).map((key) => {

            const allowedColors = new Set(Array.from({length: kFactor}, (_, i) => i));
            allowedColors.delete(coloring[key]);
            for(const [vertex, _] of graphAdjacencyList.get(key) ?? []) {
              allowedColors.delete(coloring[vertex]);
            }

            return (<NodeG
              key={key}
              ref={(e) => {
                vertexRefs.current?.set(key, e);
              }}
              colorIndexInitial={coloring[key] ?? null}
              x={vertexGraph.get(key)?.x || 0}
              y={vertexGraph.get(key)?.y || 0}
              onSelect={() => {
                deselectObjects(key, null);
              }}
              allowedColors={allowedColors}
              compromised={compromisedVertices.has(key)}
              draggable={keyDownUnblock}
              mode={nodeMode}
              whileDragging={(x, y) => {
                setVertexGraph((prev) => {
                  const newMap = new Map(prev);
                  const current = newMap.get(key);
                  if(current === undefined) return newMap;

                  newMap.set(key, {...current, xRelative: x, yRelative: y});
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
