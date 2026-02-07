# @r-dynamic-coloring/graph-canvas

A high-performance, interactive graph canvas component for React applications, designed for visualizing and manipulating graph structures with dynamic coloring support.

## Installation

```bash
pnpm add @r-dynamic-coloring/graph-canvas
```

> **Note:** Requires React 18 or higher.

## Usage

### 1. Create a Context

```tsx
'use client'

import { createGraphCanvasContext } from '@r-dynamic-coloring/graph-canvas';

export const MyGraphContext = createGraphCanvasContext();
```

### 2. Wrap with Provider

```tsx
'use client'

import { GraphCanvasProvider } from '@r-dynamic-coloring/graph-canvas';
import { MyGraphContext } from './context';

export function GraphApp({ children }) {
  return (
    <GraphCanvasProvider context={MyGraphContext}>
      {children}
    </GraphCanvasProvider>
  );
}
```

### 3. Render the Canvas

```tsx
'use client'

import { GraphCanvas } from '@r-dynamic-coloring/graph-canvas';
import { MyGraphContext } from './context';

export function GraphViewer() {
  return (
    <GraphCanvas
      context={MyGraphContext}
      styleProps={{ width: '100%', height: '600px' }}
      fontSize={14}
      nodeRadius={25}
      theme="dark"
    />
  );
}
```

### 4. Access Graph State

```tsx
'use client'

import { useGraphCanvasContext } from '@r-dynamic-coloring/graph-canvas';
import { MyGraphContext } from './context';

export function GraphControls() {
  const { clearCanvas, saveAsImage } = useGraphCanvasContext(MyGraphContext);

  return (
    <div>
      <button onClick={clearCanvas}>Clear</button>
      <button onClick={() => saveAsImage(true)}>Download PNG</button>
    </div>
  );
}
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Double Click` (empty area) | Create vertex |
| `Click` (element) | Select |
| `Drag` (vertex) | Move |
| `Delete` | Delete selected |
| `1-9`, `0` | Assign color |

## License

ISC
