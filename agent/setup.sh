#!/bin/bash

# Graph Analysis Agent - Quick Setup Script

echo "🚀 Setting up Graph Analysis Agent..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✓ UV is installed"

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your GOOGLE_API_KEY"
    echo "   You can get an API key from: https://makersuite.google.com/app/apikey"
    echo ""
else
    echo "✓ .env file exists"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies with UV..."
uv sync

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create storage directories
echo ""
echo "📁 Creating storage directories..."
mkdir -p visualizations
mkdir -p sources
echo "✓ Storage directories created"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GOOGLE_API_KEY"
echo "2. Start the server:"
echo "   uv run uvicorn api.main:app --reload"
echo ""
echo "3. Visit http://localhost:8000/docs for API documentation"
echo ""
echo "4. Or run examples:"
echo "   uv run python examples/basic_usage.py"
echo ""
