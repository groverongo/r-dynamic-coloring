.PHONY: build run test clean dev deps migrate-up migrate-down

# Application name
APP_NAME := r-dynamic-coloring-service

# Go parameters
GOCMD=go
GOBUILD=$(GOCMD) build
GOCLEAN=$(GOCMD) clean
GOTEST=$(GOCMD) test
BINARY_NAME=bin/$(APP_NAME)

# Main targets
build:
	@echo "Building $(APP_NAME)..."
	$(GOBUILD) -o $(BINARY_NAME) -v ./cmd/...

run:
	@echo "Starting $(APP_NAME)..."
	$(GOCMD) run ./cmd/...

test:
	@echo "Running tests..."
	$(GOTEST) -v ./...

clean:
	@echo "Cleaning..."
	$(GOCLEAN)
	rm -f $(BINARY_NAME)

dev:
	@echo "Starting development server with hot-reload..."
	air

deps:
	@echo "Installing dependencies..."
	go mod tidy
	go mod download

# Database migration commands (update these with your migration tool)
migrate-up:
	@echo "Running database migrations..."
	# Add your migration command here, for example:
	# migrate -path ./migrations -database "$(DATABASE_URL)" up

migrate-down:
	@echo "Reverting database migrations..."
	# Add your migration command here, for example:
	# migrate -path ./migrations -database "$(DATABASE_URL)" down

# Help command
help:
	@echo "Available commands:"
	@echo "  build     - Build the application"
	@echo "  run       - Run the application"
	@echo "  test      - Run tests"
	@echo "  clean     - Remove build artifacts"
	@echo "  dev       - Run in development mode with hot-reload (requires air)"
	@echo "  deps      - Install dependencies"
	@echo "  migrate-up   - Run database migrations"
	@echo "  migrate-down - Rollback database migrations"