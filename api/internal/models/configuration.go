package models

type Configuration struct {
	ID uint `gorm:"primaryKey"`
	R  int  `json:"r"`
	K  int  `json:"k"`
	G  int  `json:"g"`
}
