package server

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"r-hued-coloring-service/internal/config"
	"r-hued-coloring-service/internal/handler"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

type Server struct {
	echo *echo.Echo
	cfg  *config.Config
}

// New creates a new server instance
func New(cfg *config.Config) (*Server, error) {
	e := echo.New()

	// Middleware
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: []string{"*"},
		AllowMethods: []string{http.MethodGet, http.MethodHead, http.MethodPut, http.MethodPatch, http.MethodPost, http.MethodDelete},
	}))

	// Initialize handlers
	handler.InitRoutes(e)

	return &Server{
		echo: e,
		cfg:  cfg,
	}, nil
}

// Start starts the HTTP server
func (s *Server) Start() error {
	addr := fmt.Sprintf(":%d", s.cfg.Server.Port)
	log.Printf("Starting server on %s", addr)
	return s.echo.Start(addr)
}

// Shutdown gracefully shuts down the server
func (s *Server) Shutdown() error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := s.echo.Shutdown(ctx); err != nil {
		s.echo.Logger.Fatal(err)
		return err
	}

	return nil
}
