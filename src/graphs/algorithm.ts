type GraphType = Record<number, number[]>;
type BorderType = Set<number>;
type TriadType = [number, number, number];
const MIDDLE = 1;
const VERTEX_1 = 0;
const VERTEX_2 = 2;
type LocationsType = 0|1|2;
type CodeToCoordinateMapType = Record<number, [number, number]>;

const DEBUG = false;

const TOTAL_GRAPHS: {
    G: GraphType;
    B: BorderType;
    T: TriadType[];
    TriadsHistory: TriadType[];
}[] = []

function deepCopyCodeKeyObject(object: GraphType): any {
    const copiedObject = JSON.parse(JSON.stringify(object));
    const result =  Object.fromEntries(Object.entries(copiedObject).map(value => {
        return [value[0] ,value[1]]
    }))
    return result;
}

function obtainGraphs(G: GraphType, B: BorderType, T: TriadType[], mapper: CodeToCoordinateMapType, triadIndex: number = 0, TriadsHistory: TriadType[] = []){
    DEBUG && console.log('Available triads:', T.map(triad => triad.map(v => mapper[v])));
    if(T.length <= 3){
        TOTAL_GRAPHS.push({G, B, T, TriadsHistory});
        return;
    }


    let triadSelected = T[triadIndex];
    TriadsHistory.push(triadSelected)

    DEBUG && console.log('Selected triad', triadSelected.map(v => mapper[v]));
    
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
    DEBUG && console.log('Triad Vertex1 Candidates:', triadVertex1Candidates.map(triad => triad.map(v => mapper[v])));
    DEBUG && console.log('Triad Vertex2 Candidates:', triadVertex2Candidates.map(triad => triad.map(v => mapper[v])));

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

    T.forEach( (t, iT) => {
        console.log(12)
        const copyGraph = deepCopyCodeKeyObject(GRAPH);
        const copyBorder = new Set(BORDER)
        const copyTriads = JSON.parse(JSON.stringify(TRIADS))
        obtainGraphs(copyGraph, copyBorder, copyTriads, mapper, iT, [...TriadsHistory])
    });
}

function obtainGraphsStack(G: GraphType, B: BorderType, T: TriadType[], mapper: CodeToCoordinateMapType, triadIndex: number = 0, TriadsHistory: TriadType[] = []){
  const stack: { G: GraphType; B: BorderType; T: TriadType[]; triadIndex: number; TriadsHistory: TriadType[] }[] = [{ G, B, T, triadIndex, TriadsHistory }];

  while (stack.length > 0) {
    let { G, B, T, triadIndex, TriadsHistory } = stack.pop()!;

    DEBUG && console.log('Available triads:', T.map(triad => triad.map(v => mapper[v])));

    if (T.length <= 3) {
      TOTAL_GRAPHS.push({ G, B, T, TriadsHistory });
      continue;
    }

    let triadSelected = T[triadIndex];
    TriadsHistory.push(triadSelected);

    DEBUG && console.log('Selected triad', triadSelected.map(v => mapper[v]));

    let triadVertex1Candidates: TriadType[] = [];
    let triadVertex2Candidates: TriadType[] = [];

    T.forEach((triad, index) => {
      if (index === triadIndex) return;
      if (triad.includes(triadSelected[VERTEX_1])) {
        triadVertex1Candidates.push(triad);
      } else if (triad.includes(triadSelected[VERTEX_2])) {
        triadVertex2Candidates.push(triad);
      }
    });

    DEBUG && console.log('Triad Vertex1 Candidates:', triadVertex1Candidates.map(triad => triad.map(v => mapper[v])));
    DEBUG && console.log('Triad Vertex2 Candidates:', triadVertex2Candidates.map(triad => triad.map(v => mapper[v])));

    function obtainCandidateVertex(selectedTriad: TriadType, triadCandidates: TriadType[], terminalVertex: 0 | 2) {
      for (const triad of triadCandidates) {
        if (selectedTriad[terminalVertex] === triad[MIDDLE]) {
          if (selectedTriad[MIDDLE] === triad[VERTEX_1])
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
    T = T.filter(triad => triad.indexOf(triadSelected[MIDDLE]) === -1);
    T.push(triadVertex1, triadVertex2);

    B.delete(triadSelected[MIDDLE]);

    DEBUG && console.log('Result:', T.map(triad => triad.map(v => mapper[v])));

    T.forEach((t, iT) => {
      const copyGraph = deepCopyCodeKeyObject(GRAPH);
      const copyBorder = new Set(BORDER);
      const copyTriads = JSON.parse(JSON.stringify(TRIADS));
      stack.push({ G: copyGraph, B: copyBorder, T: copyTriads, triadIndex: iT, TriadsHistory: [...TriadsHistory] });
    });
  }
}

let TRIADS: TriadType[] = [[0, 1, 3], [1, 3, 6], [0, 2, 5], [2, 5, 9], [9, 8, 7], [8, 7, 6]];
let GRAPH: GraphType = {0: [1, 2], 1: [0, 2, 3, 4], 2: [0, 1, 4, 5], 3: [1, 4, 6, 7], 4: [1, 2, 3, 5, 7, 8], 5: [2, 4, 8, 9], 6: [3, 7], 7: [3, 4, 6, 8], 8: [4, 5, 7, 9], 9: [5, 8]};
let BORDER: BorderType = new Set([0, 2, 5, 9, 1, 3, 6, 8, 7]);
let toCoordinateMap: CodeToCoordinateMapType = {0: [0, 0], 1: [0, 1], 2: [1, 0], 3: [0, 2], 4: [1, 1], 5: [2, 0], 6: [0, 3], 7: [1, 2], 8: [2, 1], 9: [3, 0]}

function convertToCoordinateGraph(G: GraphType){
    return Object.fromEntries(Object.entries(G).map(value => {
        return [
            JSON.stringify(toCoordinateMap[+value[0]]),
            value[1].map(vertex => toCoordinateMap[vertex])
        ]
    }))
}
function convertToCoordinateTriads(T: TriadType[]){
    return T.map(val => val.map(v => toCoordinateMap[v]))
}
function convertToCoordinateBorder(B: BorderType){
    return Array.from(B).map( v => toCoordinateMap[v] );
}

function convertResponseToCoordinate(resp: {
    G: GraphType;
    B: BorderType;
    T: TriadType[];
    TriadsHistory: TriadType[];
}) {
    const result: any = {};
    result.G = convertToCoordinateGraph(resp.G);
    result.T = convertToCoordinateTriads(resp.T);
    result.TriadsHistory = convertToCoordinateTriads(resp.TriadsHistory);
    result.B = convertToCoordinateBorder(resp.B);

    return result;
}

for(let iTriad = 0; iTriad < 2; iTriad++){
    const copyGraph = deepCopyCodeKeyObject(GRAPH);
    const copyBorder = new Set(BORDER)
    const copyTriads = JSON.parse(JSON.stringify(TRIADS))
    obtainGraphsStack(copyGraph, copyBorder, copyTriads, toCoordinateMap, iTriad, [])
}
// for(let i = 0; i < TRIADS.length; i++) {
    // const copyGraph = deepCopyCodeKeyObject(GRAPH);
    // const copyBorder = new Set(BORDER)
    // const copyTriads = JSON.parse(JSON.stringify(TRIADS))
    // const response = obtainGraphs(copyGraph, copyBorder, copyTriads, toCoordinateMap, i)
    // outputGraphs.push(response)
    // console.info(response)
    // console.info(`[ITERATION N°${i}]`)
    // const responseCoordinate = convertResponseToCoordinate(response)
    // console.info("Graph Adjacency List:",responseCoordinate.G);
    // console.info("Border:",responseCoordinate.B);
    // console.info("Triads:",responseCoordinate.T);
    // console.info("Selected Triad History:",responseCoordinate.TriadsHistory);
// }


// console.log(convertToCoordinate(GRAPH))
// const response = obtainGraphs(GRAPH, BORDER, TRIADS, toCoordinate);
//// console.log(response)
// console.log(convertToCoordinate(response.G))
