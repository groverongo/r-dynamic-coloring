package models

type Assignment struct {
	Id              uint          `gorm:"primaryKey"`
	GraphId         uint          `json:"graphId"`
	ConfigurationId uint          `json:"configurationId"`
	Coloring        string        `json:"coloring"`
	Configuration   Configuration `gorm:"foreignKey:Id;references:ConfigurationId"`
	Graph           Graph         `gorm:"foreignKey:Id;references:GraphId"`
}
