package models

import (
	"r-hued-coloring-service/internal/validation"
	"time"

	"github.com/google/uuid"
)

type Graph struct {
	Id            string `gorm:"primaryKey"`
	Name          string `json:"name"`
	AdjacencyList string `json:"adjacencyList"`
	DisplayList   string `json:"displayList"`
	CreatedAt     time.Time
	UpdatedAt     time.Time
}

func (g *Graph) Create(r validation.CreateGraphRequest) error {
	g.Name = r.Name
	g.AdjacencyList = r.AdjacencyList
	g.DisplayList = r.DisplayList
	g.CreatedAt = time.Now()
	g.UpdatedAt = time.Now()
	g.Id = uuid.New().String()
	return nil
}
