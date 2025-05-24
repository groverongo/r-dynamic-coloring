type GraphType = Record<number, number[]>;
type BorderType = Set<number>;
type TriadType = [number, number, number];
const MIDDLE = 1;
const VERTEX_1 = 0;
const VERTEX_2 = 2;
type LocationsType = 0|1|2;

function obtainGraphs(G: GraphType, B: BorderType, T: TriadType[]){
    let triadIndex = 0;
    let triadSelected = T.at(triadIndex);
    if(triadSelected === undefined)
        return G;

    B.delete(triadSelected[MIDDLE]);

    let triadRemoveIndexes: number[] = [];
    T.forEach( (triad, index) => {
        if(triadSelected[MIDDLE] === triad[MIDDLE])
            triadRemoveIndexes.push(index);
    });

    let triadVertex1Candidates: TriadType[] = [];
    let triadVertex2Candidates: TriadType[] = [];
    T.forEach( (triad, index) => {
        if(index === triadIndex) return;

        if(triad.includes(triadSelected[VERTEX_1])){
            triadVertex1Candidates.push(triad);
        }
        else if(triad.includes(triadSelected[VERTEX_2])){
            triadVertex2Candidates.push(triad);
        }
    });

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
        obtainCandidateVertex(triadSelected, triadVertex1Candidates, VERTEX_2)
    ];
    
    G[triadSelected[VERTEX_1]].push(triadSelected[VERTEX_2]);
    G[triadSelected[VERTEX_2]].push(triadSelected[VERTEX_1]);

    T.splice(triadIndex);
    T.push(triadVertex1, triadVertex2);

    B.delete(triadSelected[MIDDLE]);
}