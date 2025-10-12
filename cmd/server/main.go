package main

import (
	"log"
	"os"
	"os/signal"
	"r-hued-coloring-service/internal/config"
	"r-hued-coloring-service/internal/server"
	"r-hued-coloring-service/internal/validation"
	"syscall"
)

func main() {
	// Load configuration
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}

	// Initialize and start the server
	srv, err := server.New(cfg)
	if err != nil {
		log.Fatalf("Failed to create server: %v", err)
	}

	// Initialize validation
	validation.Init()

	// Start server in a goroutine
	go func() {
		if err := srv.Start(); err != nil {
			log.Printf("Server error: %v", err)
		}
	}()

	// Wait for interrupt signal to gracefully shut down the server
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)
	<-quit

	log.Println("Shutting down server...")
	if err := srv.Shutdown(); err != nil {
		log.Fatalf("Server shutdown failed: %v", err)
	}
	log.Println("Server exited properly")
}
