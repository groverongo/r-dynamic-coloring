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
	Database struct {
		Host     string
		User     string
		Password string
		DBName   string
		Port     int
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

	// Database configuration
	cfg.Database.Host = getEnv("DATABASE_HOST", "localhost")
	cfg.Database.User = getEnv("DATABASE_USER", "postgres")
	cfg.Database.Password = getEnv("DATABASE_PASSWORD", "postgres")
	cfg.Database.DBName = getEnv("DATABASE_DBNAME", "postgres")
	port, err = strconv.Atoi(getEnv("DATABASE_PORT", "5432"))
	if err != nil {
		return nil, fmt.Errorf("invalid DATABASE_PORT: %v", err)
	}
	cfg.Database.Port = port

	return &cfg, nil
}

func (c *Config) DSN() string {
	return fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%d sslmode=disable",
		c.Database.Host,
		c.Database.User,
		c.Database.Password,
		c.Database.DBName,
		c.Database.Port,
	)
}

// getEnv gets an environment variable or returns a default value
func getEnv(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return defaultValue
}
