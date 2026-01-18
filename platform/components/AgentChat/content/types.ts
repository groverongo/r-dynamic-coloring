export interface CustomMessage {
    type: 'request' | 'response';
    data: string;
    timestamp: string;
    id: string;
}