package database

import (
	"fmt"

	"r-hued-coloring-service/internal/config"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var dbInstance *gorm.DB

// NewDatabase creates a new database connection
func NewDatabase(cfg *config.Config) error {
	dsn := cfg.DSN()
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		return fmt.Errorf("failed to connect to database: %v", err)
	}

	// Enable debug mode in development
	if cfg.App.Env == "development" {
		db = db.Debug()
	}

	dbInstance = db

	return nil
}

func GetDB() *gorm.DB {
	return dbInstance
}
