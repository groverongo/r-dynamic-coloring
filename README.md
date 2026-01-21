# R-Hued Coloring Platform

A comprehensive platform for graph coloring research and visualization, combining algorithm development, API services, AI agents, and an interactive web interface.

🔗 **Live Demo**: [https://r-hued-coloring-platform.vercel.app/](https://r-hued-coloring-platform.vercel.app/)

## Project Structure

This monorepo contains five main components:

### 📊 [`platform`](/platform)

Next.js-based web application providing an interactive chat interface for graph coloring research and visualization.

**Tech Stack:**
- **Framework:** Next.js 16 with App Router, React 19
- **AI Integration:** Vercel AI SDK with support for multiple LLM providers (xAI, OpenAI, etc.)
- **UI:** React with Tailwind CSS, Radix UI components
- **Visualization:** Konva.js for graph rendering and manipulation
- **Authentication:** Auth.js (NextAuth.js)
- **Storage:** Vercel Blob for file storage

**Key Features:**
- Interactive chat interface for graph coloring queries
- Real-time graph visualization and editing
- Support for multiple AI models through Vercel AI Gateway
- Responsive design with dark/light theme support
- Code highlighting and markdown rendering

**Development:**
```bash
cd platform
pnpm install
pnpm dev
```


---

### 🎨 [`packages/GraphCanvas`](/packages/GraphCanvas)

A high-performance, reusable React component library for interactive graph visualization and manipulation, specifically designed for r-hued coloring research.

**Tech Stack:**
- **Language:** TypeScript 5.9+
- **Framework:** React 19 with React Konva
- **Canvas Rendering:** Konva.js, react-konva, react-konva-utils
- **SVG Processing:** canvg, svgson, tex-to-svg
- **Build Tool:** tsup for bundling

**Key Features:**
- Interactive graph canvas with drag-and-drop vertex positioning
- Real-time edge creation and manipulation
- R-hued coloring visualization with customizable color palettes
- Graph state management through React Context API
- Export graphs as PNG images (download or clipboard)
- Support for vertex labeling and coloring modes
- Keyboard shortcuts for efficient graph editing
- Type-safe API with full TypeScript support

**Components:**
- `GraphCanvas` - Main canvas component for graph rendering
- `GraphCanvasProvider` - Context provider for graph state management
- `Vertex` - Interactive vertex component with customizable styling
- `Edge` - Dynamic edge component with curved line rendering
- `TemporaryEdge` - Visual feedback for edge creation

**Installation:**
```bash
pnpm add @r-dynamic-coloring/graph-canvas
```

**Usage:**
```typescript
import { GraphCanvas, GraphCanvasProvider, createGraphCanvasContext } from '@r-dynamic-coloring/graph-canvas';

const MyGraphContext = createGraphCanvasContext();

function App() {
  return (
    <GraphCanvasProvider context={MyGraphContext}>
      <GraphCanvas context={MyGraphContext} />
    </GraphCanvasProvider>
  );
}
```

---

### 🚀 [`api`](/api)

RESTful API service built with Go and Echo framework, providing backend services for graph data management and authentication.

**Tech Stack:**
- **Language:** Go 1.25+
- **Framework:** Echo v4 (web framework)
- **Database:** PostgreSQL with GORM ORM
- **Validation:** go-playground/validator
- **Authentication:** JWT (golang-jwt/jwt)

**Key Features:**
- RESTful endpoints for graph operations
- Database models and migrations using GORM
- Request validation and error handling
- JWT-based authentication
- PostgreSQL integration for data persistence

**Development:**
```bash
cd api
make run
```

---

### 🧮 [`model`](/model)

Python-based computational engine implementing graph coloring algorithms and mathematical models.

**Tech Stack:**
- **Language:** Python 3.13+
- **Framework:** FastAPI for API endpoints
- **Libraries:** NetworkX, NumPy, Pandas, Matplotlib, PuLP

**Key Features:**
- Graph generation utilities (circulant, planar 3-trees, Eulerian graphs, etc.)
- R-hued coloring algorithms and validation
- Linear programming solvers for optimization problems
- Graph visualization and analysis tools
- FastAPI endpoints for model computations

**Development:**
```bash
cd model
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -e .
uvicorn main.api.main:app --reload
```

---

### 🤖 [`agent`](/agent)

LangGraph-based AI agent service for intelligent graph analysis and research assistance.

**Tech Stack:**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **AI Libraries:** LangChain, LangGraph, LangChain Google GenAI, LangChain Groq

**Key Features:**
- Conversational AI agent for graph theory research
- Integration with multiple LLM providers (Google GenAI, Groq)
- State management with LangGraph for multi-turn conversations
- Custom nodes for graph-specific reasoning
- FastAPI endpoints for agent invocation

**Development:**
```bash
cd agent
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -e .
uvicorn src:app --reload
```

---

## Getting Started

### Prerequisites
- Node.js 18+ and pnpm (for platform)
- Go 1.25+ (for api)
- Python 3.11+ (for agent and model)
- Docker and Docker Compose (optional, for containerized deployment)
- PostgreSQL 14+ (for persistent storage)

### Quick Start with Docker Compose

```bash
# Start all services
docker-compose up

# Platform: http://localhost:3000
# API: http://localhost:8080
# Model: http://localhost:8000
# Agent: http://localhost:8001
```

### Configuration

Each service has its own environment configuration:
- `platform/.env` - Next.js app configuration
- `api/.env` - API server configuration
- `model/.env` - Model service configuration
- `agent/.env` - Agent service configuration

Refer to `.env.example` or `.env.template` files in each directory for required variables.

## Development Workflow

1. **Platform Development**: Work on UI/UX features in the `platform` directory
2. **API Development**: Build backend services in the `api` directory
3. **Model Development**: Implement algorithms in the `model` directory
4. **Agent Development**: Enhance AI capabilities in the `agent` directory

## Contributing

Contributions are welcome! Please ensure:
- Code follows the style guidelines of each service
- Tests pass before submitting PRs
- Documentation is updated accordingly
