package models

import (
	"r-hued-coloring-service/internal/validation"
	"time"

	"github.com/google/uuid"
)

type Message struct {
	ID        string    `gorm:"primaryKey" json:"id"`
	Content   string    `json:"content"`
	CreatedAt time.Time `json:"createdAt"`
	UpdatedAt time.Time `json:"updatedAt"`
}

type Conversation struct {
	ID        string    `gorm:"primaryKey" json:"id"`
	GraphId   string    `gorm:"foreignKey:GraphId;references:ID"`
	Messages  []Message `json:"messages"`
	CreatedAt time.Time `json:"createdAt"`
	UpdatedAt time.Time `json:"updatedAt"`
}

func (c *Conversation) Create(r validation.CreateConversationRequest) error {
	c.GraphId = r.GraphId
	c.CreatedAt = time.Now()
	c.UpdatedAt = time.Now()
	c.ID = uuid.New().String()
	return nil
}
