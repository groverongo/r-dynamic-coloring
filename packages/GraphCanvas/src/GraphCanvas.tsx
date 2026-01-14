import { useEffect, useRef } from 'react';

export interface GraphCanvasProps {
    /**
     * Data representing the graph (e.g., nodes and edges)
     */
    data?: any;
    /**
     * Custom width for the canvas
     */
    width?: number | string;
    /**
     * Custom height for the canvas
     */
    height?: number | string;
    /**
     * Optional callback when a node is clicked
     */
    onNodeClick?: (node: any) => void;
    /**
     * Additional CSS classes
     */
    className?: string;
}

/**
 * GraphCanvas Component
 * A template for rendering dynamic graphs using HTML5 Canvas in React.
 */
export const GraphCanvas = ({
    width = '100%',
    height = '400px',
    className = '',
    onNodeClick,
}: GraphCanvasProps) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // Handle resizing
        const resizeCanvas = () => {
            const parent = canvas.parentElement;
            if (parent) {
                canvas.width = parent.clientWidth;
                canvas.height = parent.clientHeight;
                drawTemplate();
            }
        };

        const drawTemplate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw a subtle background gradient
            const gradient = ctx.createRadialGradient(
                canvas.width / 2, canvas.height / 2, 0,
                canvas.width / 2, canvas.height / 2, Math.max(canvas.width, canvas.height)
            );
            gradient.addColorStop(0, '#1a1a1a');
            gradient.addColorStop(1, '#0a0a0a');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw some placeholder nodes
            const nodes = [
                { x: canvas.width * 0.3, y: canvas.height * 0.5, color: '#3b82f6' },
                { x: canvas.width * 0.7, y: canvas.height * 0.5, color: '#ef4444' },
                { x: canvas.width * 0.5, y: canvas.height * 0.3, color: '#10b981' },
            ];

            // Draw edges
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(nodes[0].x, nodes[0].y);
            ctx.lineTo(nodes[1].x, nodes[1].y);
            ctx.lineTo(nodes[2].x, nodes[2].y);
            ctx.lineTo(nodes[0].x, nodes[0].y);
            ctx.stroke();

            // Draw nodes
            nodes.forEach(node => {
                ctx.beginPath();
                ctx.arc(node.x, node.y, 10, 0, Math.PI * 2);
                ctx.fillStyle = node.color;
                ctx.shadowBlur = 15;
                ctx.shadowColor = node.color;
                ctx.fill();
                ctx.shadowBlur = 0;
            });

            // Text placeholder
            ctx.fillStyle = '#666';
            ctx.font = '14px Inter, system-ui, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('GraphCanvas Template Ready', canvas.width / 2, canvas.height - 20);
        };

        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        return () => {
            window.removeEventListener('resize', resizeCanvas);
        };
    }, []);

    return (
        <div
            className={`graph-canvas-container ${className}`}
            style={{
                width,
                height,
                position: 'relative',
                overflow: 'hidden',
                borderRadius: '8px',
                border: '1px solid #333'
            }}
        >
            <canvas
                ref={canvasRef}
                style={{ display: 'block' }}
            />
        </div>
    );
};
