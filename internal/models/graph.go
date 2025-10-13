package models

import (
	"time"
)

type Graph struct {
	Id            string `gorm:"primaryKey"`
	Name          string `json:"name"`
	AdjacencyList string `json:"adjacencyList"`
	DisplayList   string `json:"displayList"`
	CreatedAt     time.Time
	UpdatedAt     time.Time
}
