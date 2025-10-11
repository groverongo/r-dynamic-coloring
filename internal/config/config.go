package config

import (
	"fmt"
	"os"
	"strconv"
)

type Config struct {
	Server struct {
		Port int
	}
	App struct {
		Name    string
		Version string
		Env     string
	}
}

// Load loads the configuration from environment variables
func Load() (*Config, error) {
	var cfg Config

	// Server configuration
	port, err := strconv.Atoi(getEnv("SERVER_PORT", "8080"))
	if err != nil {
		return nil, fmt.Errorf("invalid SERVER_PORT: %v", err)
	}
	cfg.Server.Port = port

	// App configuration
	cfg.App.Name = getEnv("APP_NAME", "r-dynamic-coloring-service")
	cfg.App.Version = getEnv("APP_VERSION", "0.1.0")
	cfg.App.Env = getEnv("APP_ENV", "development")

	return &cfg, nil
}

// getEnv gets an environment variable or returns a default value
func getEnv(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return defaultValue
}
