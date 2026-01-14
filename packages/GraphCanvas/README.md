# @r-dynamic-coloring/graph-canvas

A high-performance, dynamic graph rendering component for React applications. This package is part of the `r-dynamic-coloring` monorepo.

## Installation

```bash
pnpm add @r-dynamic-coloring/graph-canvas
```

## Usage

```tsx
import { GraphCanvas } from '@r-dynamic-coloring/graph-canvas';

function App() {
  return (
    <div style={{ width: '800px', height: '600px' }}>
      <GraphCanvas />
    </div>
  );
}
```

## Features

- **Responsive**: Automatically scales to fit its container.
- **Performant**: Built with HTML5 Canvas for smooth animations and large datasets.
- **Customizable**: Extensive props for styling and behavior control.

## Development

To start the development server with hot-reloading:

```bash
pnpm dev
```

To build the package for production:

```bash
pnpm build
```

## License

ISC
