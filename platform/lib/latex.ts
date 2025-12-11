import { CSSProperties } from "react";
import { edgeGraphType, vertexGraphType } from "./atoms";

export class GraphTikz {

    private _uuidToInt: Record<string, number>;
    private _vertices: vertexGraphType;
    private _edges: edgeGraphType;
    private _boardDimensions: [number, number]; // [width, height]
    private _scaleFactor: number = 5;
    private _aspectRatio: number; // for width product

    private createUUIDToInt(){
        const mapper: Record<string, number> = {}
        let index = 0;
        for(const key of this._vertices.keys()) {
            mapper[key] = index++;
        }
        return mapper;
    }
    
    constructor(vertices: vertexGraphType, edges: edgeGraphType, {width, height}: CSSProperties){
        console.log(vertices)
        this._vertices = vertices;
        this._edges = edges;
        this._uuidToInt = this.createUUIDToInt();
        if(!width || !height)
            throw Error(`Undefined width ${width}, or height ${height}`);
        this._boardDimensions = [+width, +height];
        this._aspectRatio = this._boardDimensions[0] / this._boardDimensions[1];
    }

    private vertexLabel = (label: number) => `(V_${label})`;
    private drawVertex (uuidLabel: string, position: [number, number], text?: string) {
        const intLabel: number = this._uuidToInt[uuidLabel];
        const convertedPositions: [number, number] = [
            (position[0] / this._boardDimensions[0]) * this._scaleFactor * this._aspectRatio, 
            ((this._boardDimensions[1] - position[1]) / this._boardDimensions[1]) * this._scaleFactor
        ];
        const line = `\\node[vertex] ${this.vertexLabel(intLabel)} at (${convertedPositions[0]}, ${convertedPositions[1]}) {${text ?? intLabel}};`;
        return line;
    }
    
    private drawEdge (uuidLabels: [string, string]) {
        const connectStmt = uuidLabels.map((v) => this.vertexLabel(this._uuidToInt[v])).join(' -- ');
        const line = `\\draw ${connectStmt} -- cycle;`;
        return line;
    }

    private format = (
        vertices: string[], 
        edges: string[]
    ): string => `\\begin{tikzpicture}[scale=1, shorten >=1pt,->]
    \\tikzstyle{vertex}=[circle,fill=black!25,minimum size=12pt,inner sep=2pt]
    ${vertices.join('\n\t')}
    ${edges.join('\n\t')}
\\end{tikzpicture}`

    public Picture() {
        const vertexStmts: string[] = [];
        for(const [k, v] of this._vertices.entries()) {
            const stmt = this.drawVertex(k, [v.xRelative, v.yRelative])
            vertexStmts.push(stmt);
        }
        
        const edgeStmts: string[] = [];
        for(const e of this._edges.values()) {
            const stmt = this.drawEdge([e.from, e.to])
            edgeStmts.push(stmt);
        }

        const latexBlock = this.format(vertexStmts, edgeStmts);

        return latexBlock;
    }
};
