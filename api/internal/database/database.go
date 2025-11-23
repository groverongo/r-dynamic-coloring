package database

import (
	"fmt"
	"time"

	"r-hued-coloring-service/internal/config"
	"r-hued-coloring-service/internal/models"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var dbInstance *gorm.DB

// NewDatabase creates a new database connection
func NewDatabase(cfg *config.Config) error {
	dsn := cfg.DSN()

	for i := 0; i < cfg.Database.RetryAttempts; i++ {
		db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
		if err != nil {
			if i == cfg.Database.RetryAttempts-1 {
				return fmt.Errorf("failed to connect to database after %d attempts: %v", cfg.Database.RetryAttempts, err)
			} else {
				fmt.Printf("Database connection attempt %d failed: %v\n", i+1, err)
				// Sleep before retrying
				time.Sleep(time.Duration(cfg.Database.RetryDelayMs) * time.Millisecond)
				continue
			}
		}

		fmt.Printf("Database connection successful on attempt %d\n", i+1)

		// Enable debug mode in development
		if cfg.App.Env == "development" {
			db = db.Debug()
			// db.Migrator().DropTable(&models.Assignment{}, &models.Configuration{}, &models.Graph{})
		}

		// Migrate the database schema
		db.AutoMigrate(&models.Assignment{}, &models.Configuration{}, &models.Graph{})

		dbInstance = db
		break
	}

	return nil
}

func GetDB() *gorm.DB {
	return dbInstance
}
