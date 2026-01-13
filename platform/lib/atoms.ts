import { atom } from "jotai";
import { ColoringAssigmentResponse } from "./validation";
import { CSSProperties } from "react";

export const screenRatioAtom = atom(0);

export const themeAtom = atom<'light' | 'dark'>('dark');

export const graphNameAtom = atom<string>("Untitled");

export const nodeRadiusAtom = atom<number>(30);
export const fontSizeAtom = atom<number>(20);

export const stylePropsAtom = atom<CSSProperties>({});