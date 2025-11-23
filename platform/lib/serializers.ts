export class GraphSerializer {
    static vertexGraphSerializer(value: Map<string, {
        x: number;
        y: number;
        xRelative: number;
        yRelative: number;
    }>): string {
        const result: Record<string, object> = {};
        for(const [k, v] of value.entries()) {
            result[k] = v;
        }
        return JSON.stringify(result);
    }

    static edgeGraphSerializer(value: Map<string, {
        from: string;
        to: string;
        fromEntry: [string, string];
        toEntry: [string, string];
    }>): string {
        const result: Record<string, object> = {};
        for(const [k, v] of value.entries()) {
            result[k] = v;
        }
        return JSON.stringify(result);
    }

    static graphAdjacencyListSerializer(value: Map<string, Set<[string, string]>>): string {
        const adjacencyList: Record<string, [string, string][]> = {};
        for(const [vertex, edges] of value) {
            adjacencyList[vertex] = Array.from(edges);
        }
        return JSON.stringify(adjacencyList);
    }

    static simpleGraphAdjacencyListSerializer(value: Map<string, Set<[string, string]>>): string {
        const adjacencyList: Record<string, string[]> = {};
        for(const [vertex, edges] of value) {
            adjacencyList[vertex] = Array.from(edges).map(([to, _]) => to);
        }
        return JSON.stringify(adjacencyList, null, 2);
    }

    static coloringSerializer(value: Record<string, number>): string {
        return JSON.stringify(value);
    }
};

export class GraphDeserializer {
    static vertexGraphDeserializer(value: string): Map<string, {
        x: number;
        y: number;
        xRelative: number;
        yRelative: number;
    }> {
        const result: Map<string, {
            x: number;
            y: number;
            xRelative: number;
            yRelative: number;
        }> = new Map<string, {
            x: number;
            y: number;
            xRelative: number;
            yRelative: number;
        }>();
        const parsed = JSON.parse(value);
        for(const [k, v] of Object.entries(parsed)) {
            result.set(k, v as any);
        }
        return result;
    }

    static edgeGraphDeserializer(value: string): Map<string, {
        from: string;
        to: string;
        fromEntry: [string, string];
        toEntry: [string, string];
    }> {
        const result: Map<string, {
            from: string;
            to: string;
            fromEntry: [string, string];
            toEntry: [string, string];
        }> = new Map<string, {
            from: string;
            to: string;
            fromEntry: [string, string];
            toEntry: [string, string];
        }>();
        const parsed = JSON.parse(value);
        for(const [k, v] of Object.entries(parsed)) {
            result.set(k, v as any);
        }
        return result;
    }

    static graphAdjacencyListDeserializer(value: string): Map<string, Set<[string, string]>> {
        const result: Map<string, Set<[string, string]>> = new Map<string, Set<[string, string]>>();
        const parsed = JSON.parse(value);
        for(const [k, v] of Object.entries(parsed)) {
            result.set(k, new Set(v as any));
        }
        return result;
    }

    static simpleGraphAdjacencyListDeserializer(value: string): Map<string, Set<[string, string]>> {
        const result: Map<string, Set<[string, string]>> = new Map<string, Set<[string, string]>>();
        const parsed = JSON.parse(value);
        for(const [k, v] of Object.entries(parsed)) {
            result.set(k, new Set(v as any));
        }
        return result;
    }

    static coloringDeserializer(value: string): Record<string, number> {
        const result: Record<string, number> = {};
        const parsed = JSON.parse(value);
        for(const [k, v] of Object.entries(parsed)) {
            result[k] = v as number;
        }
        return result;
    }
}