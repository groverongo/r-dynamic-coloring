package models

import (
	"r-hued-coloring-service/internal/validation"
	"time"

	"github.com/google/uuid"
)

type Graph struct {
	ID                 string `gorm:"primaryKey"`
	Name               string `json:"name"`
	GraphAdjacencyList string `json:"graphAdjacencyList"`
	VertexGraph        string `json:"vertexGraph"`
	EdgeGraph          string `json:"edgeGraph"`
	LocalColoring      string `json:"localColoring"`
	LocalR             uint   `json:"localR"`
	LocalK             uint   `json:"localK"`
	CreatedAt          time.Time
	UpdatedAt          time.Time
}

func (g *Graph) Create(r validation.CreateGraphRequest) error {
	g.Name = r.Name
	g.GraphAdjacencyList = r.GraphAdjacencyList
	g.VertexGraph = r.VertexGraph
	g.EdgeGraph = r.EdgeGraph
	g.LocalColoring = r.LocalColoring
	g.LocalR = r.LocalR
	g.LocalK = r.LocalK
	g.CreatedAt = time.Now()
	g.UpdatedAt = time.Now()
	g.ID = uuid.New().String()
	return nil
}
