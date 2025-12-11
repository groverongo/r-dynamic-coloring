import { atom } from "jotai";
import { ColoringAssigmentResponse } from "./validation";
import { CSSProperties } from "react";

export const screenRatioAtom = atom(0);

export const themeAtom = atom<'light' | 'dark'>('light');

export const vertexCurrentIdAtom = atom<string | null>(null);

export const edgeCurrentIdAtom = atom<string | null>(null);

export const coloringAtom = atom<ColoringAssigmentResponse>({});
export const rFactorAtom = atom<number>(1);
export const kColorsAtom = atom<number>(1);

export const graphNameAtom = atom<string>("Untitled");

export const nodeRadiusAtom = atom<number>(30);
export const fontSizeAtom = atom<number>(20);

export const stylePropsAtom = atom<CSSProperties>({});

export type graphAdjacencyListType = Map<string, Set<[string, string]>>;
export const graphAdjacencyListAtom = atom<graphAdjacencyListType>(new Map<string, Set<[string, string]>>());

export type vertexGraphType = Map<string, {x: number, y: number, xRelative: number, yRelative: number}>;
export const vertexGraphAtom = atom<vertexGraphType>(new Map<string, {x: number, y: number, xRelative: number, yRelative: number}>());

export type edgeGraphType = Map<string, {from: string, to: string, fromEntry: [string, string], toEntry: [string, string]}>;
export const edgeGraphAtom = atom<edgeGraphType>(new Map<string, {from: string, to: string, fromEntry: [string, string], toEntry: [string, string]}>());

