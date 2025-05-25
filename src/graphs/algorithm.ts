type GraphType = Record<number, number[]>;
type BorderType = Set<number>;
type TriadType = [number, number, number];
const MIDDLE = 1;
const VERTEX_1 = 0;
const VERTEX_2 = 2;
type LocationsType = 0|1|2;
type CodeToCoordinateMapType = Record<number, [number, number]>;

const DEBUG = false;

function obtainGraphs(G: GraphType, B: BorderType, T: TriadType[], iterations: number, mapper: CodeToCoordinateMapType){
    console.log(`Available triads:`, T.map(triad => triad.map(v => mapper[v])));
    for(let i = 0; i < iterations && T.length > 3; i++){

        let triadIndex = 0;
        let triadSelected = T[triadIndex];

        DEBUG && console.log("Selected triad", triadSelected.map(v => mapper[v]));
        
        let triadVertex1Candidates: TriadType[] = [] //T.filter((triad, index) => index !== triadIndex && triad.includes(triadSelected[VERTEX_1]));
        let triadVertex2Candidates: TriadType[] = [] //T.filter((triad, index) => index !== triadIndex && triad.includes(triadSelected[VERTEX_2]));
        T.forEach( (triad, index) => {
            if(index === triadIndex) return;
            
            if(triad.includes(triadSelected[VERTEX_1])){
                triadVertex1Candidates.push(triad);
            }
            else if(triad.includes(triadSelected[VERTEX_2])){
                triadVertex2Candidates.push(triad);
            }
        });
        DEBUG && console.log(`Triad Vertex1 Candidates:`, triadVertex1Candidates.map(triad => triad.map(v => mapper[v])));
        DEBUG && console.log(`Triad Vertex2 Candidates:`, triadVertex2Candidates.map(triad => triad.map(v => mapper[v])));
    
        function obtainCandidateVertex(selectedTriad: TriadType, triadCandidates: TriadType[], terminalVertex: 0|2) {
            for(const triad of triadCandidates){
                if(selectedTriad[terminalVertex] === triad[MIDDLE]){
                    if(selectedTriad[MIDDLE] === triad[VERTEX_1])
                        return triad[VERTEX_2];
                    else
                        return triad[VERTEX_1];
                } else {
                    return triad[MIDDLE];
                }
            }
            throw new Error("No candidates");
        }
    
        const triadVertex1: TriadType = [
            obtainCandidateVertex(triadSelected, triadVertex1Candidates, VERTEX_1),
            triadSelected[VERTEX_1],
            triadSelected[VERTEX_2]
        ];
        
        const triadVertex2: TriadType = [
            triadSelected[VERTEX_1],
            triadSelected[VERTEX_2],
            obtainCandidateVertex(triadSelected, triadVertex2Candidates, VERTEX_2)
        ];
        
        G[triadSelected[VERTEX_1]].push(triadSelected[VERTEX_2]);
        G[triadSelected[VERTEX_2]].push(triadSelected[VERTEX_1]);
    
        T.splice(triadIndex, 1);
        T = T.filter(triad => triad.indexOf(triadSelected[MIDDLE]) === -1)
        T.push(triadVertex1, triadVertex2);
    
        B.delete(triadSelected[MIDDLE]);
    
        DEBUG && console.log('Result:', T.map(triad => triad.map(v => mapper[v])));
    }

    return {G, B, T};
}

let TRIADS: TriadType[] = [[0, 1, 3], [1, 3, 6], [0, 2, 5], [2, 5, 9], [9, 8, 7], [8, 7, 6]];
let GRAPH: GraphType = {0: [1, 2], 1: [0, 2, 3, 4], 2: [0, 1, 4, 5], 3: [1, 4, 6, 7], 4: [1, 2, 3, 5, 7, 8], 5: [2, 4, 8, 9], 6: [3, 7], 7: [3, 4, 6, 8], 8: [4, 5, 7, 9], 9: [5, 8]};
let BORDER: BorderType = new Set([0, 2, 5, 9, 1, 3, 6, 8, 7]);
let toCoordinate: CodeToCoordinateMapType = {0: [0, 0], 1: [0, 1], 2: [1, 0], 3: [0, 2], 4: [1, 1], 5: [2, 0], 6: [0, 3], 7: [1, 2], 8: [2, 1], 9: [3, 0]}
 
const response = obtainGraphs(GRAPH, BORDER, TRIADS, Infinity, toCoordinate);
console.log(response)