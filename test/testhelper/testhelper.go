package testhelper

import (
	"net/http/httptest"
	"r-dynamic-coloring-service/internal/config"
	"r-dynamic-coloring-service/internal/server"
)

// SetupTestServer creates a new test server instance for testing
func SetupTestServer() (*server.Server, *httptest.Server) {
	// Create a test configuration
	cfg := &config.Config{
		Server: struct{ Port int }{{"port": 0}}, // 0 means use any available port
		App: struct{ Name, Version, Env }{{
			Name:    "test",
			Version: "test",
			Env:     "test",
		}},
	}

	// Create a new server instance
	srv, err := server.New(cfg)
	if err != nil {
		panic(err)
	}

	// Create a test HTTP server
	testServer := httptest.NewServer(srv.Echo)

	return srv, testServer
}
