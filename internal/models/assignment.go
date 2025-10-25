package models

type Assignment struct {
	ID              uint          `gorm:"primaryKey"`
	GraphId         string        `json:"graphId"`
	ConfigurationId uint          `json:"configurationId"`
	Coloring        string        `json:"coloring"`
	Configuration   Configuration `gorm:"foreignKey:ConfigurationId;references:ID"`
	Graph           Graph         `gorm:"foreignKey:GraphId;references:ID"`
}
