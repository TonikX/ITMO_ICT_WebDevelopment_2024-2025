# Build stage
FROM golang:1.23-alpine AS builder

WORKDIR /build

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build the binary
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o printing_house cmd/main.go

# Final stage
FROM alpine:latest

WORKDIR /app

# Copy the binary from builder
COPY --from=builder /build/printing_house .

# Copy config files
COPY deployment/config/config.yml .
COPY .env.example .env

EXPOSE 8080

# Run the application
CMD ["./printing_house"]