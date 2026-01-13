'use client';

import { createGraphCanvasContext } from "@/components/graphCanvas/useContext";


export const GREEK_LETTER_NAMES = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega'];

export const SNAP_TO_PADDING = 6;
export const HIT_TARGET_PADDING = 6; 

export const MainCanvasContext = createGraphCanvasContext();