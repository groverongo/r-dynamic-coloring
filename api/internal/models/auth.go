package models

import (
	"errors"
	"r-hued-coloring-service/internal/validation"

	"github.com/google/uuid"
)

type User struct {
	ID       string `gorm:"primaryKey"`
	Email    string `gorm:"unique"`
	Password string `gorm:"not null"`
}

func (u *User) CreateFromRegisterRequest(request validation.RegisterRequest) error {

	if request.Password != request.RepeatPassword {
		return errors.New("passwords do not match")
	}

	u.ID = uuid.New().String()
	u.Email = request.Email
	u.Password = request.Password
	return nil
}

func (u *User) CreateFromLoginRequest(request validation.LoginRequest) error {
	u.Email = request.Email
	u.Password = request.Password
	return nil
}
