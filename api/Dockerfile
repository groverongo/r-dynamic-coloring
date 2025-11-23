FROM golang:1.25.2-alpine AS builder

WORKDIR /build

# Install build dependencies
RUN apk add --no-cache gcc musl-dev

# Copy go mod and sum files first for better layer caching
COPY go.mod go.sum ./

# Download all dependencies
RUN go mod download

# Copy the source code
COPY . .

# Build the application
RUN CGO_ENABLED=1 GOOS=linux go build -o output ./cmd/server

# Final stage
FROM alpine:3.19

RUN adduser -D -g '' hostuser

WORKDIR /app

# Install runtime dependencies
RUN apk --no-cache add ca-certificates

# Copy the binary from builder
COPY --from=builder /build/output .

# Give permissions
RUN chown hostuser:hostuser ./output

# Switch to non-root user
USER hostuser

# Expose port (optional)
EXPOSE 8080

# Start the server
CMD ["./output"]