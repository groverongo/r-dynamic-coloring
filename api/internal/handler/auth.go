package handler

import (
	"net/http"
	"r-hued-coloring-service/internal/database"
	"r-hued-coloring-service/internal/models"
	"r-hued-coloring-service/internal/validation"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/labstack/echo/v4"
)

type jwtCustomClaims struct {
	Name  string `json:"name"`
	Admin bool   `json:"admin"`
	jwt.RegisteredClaims
}

func Login(c echo.Context) error {
	var request validation.LoginRequest
	if err := c.Bind(&request); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]interface{}{
			"status": "ERROR",
			"error":  err.Error(),
		})
	}

	if err := request.Validate(); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]interface{}{
			"status": "ERROR",
			"error":  err.Error(),
		})
	}

	user := models.User{}
	if err := user.CreateFromLoginRequest(request); err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  err.Error(),
		})
	}

	if err := database.GetDB().Model(&models.User{}).Where("email = ?", user.Email, "password = ?", user.Password).Find(&user).Error; err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  err.Error(),
		})
	}

	claims := &jwtCustomClaims{
		user.ID,
		true,
		jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(time.Minute * 30)),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	t, err := token.SignedString([]byte("secret"))
	if err != nil {
		return err
	}

	return c.JSON(http.StatusOK, echo.Map{
		"token": t,
	})
}

func Register(c echo.Context) error {
	var request validation.RegisterRequest
	if err := c.Bind(&request); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]interface{}{
			"status": "ERROR",
			"error":  err.Error(),
		})
	}

	if err := request.Validate(); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]interface{}{
			"status": "ERROR",
			"error":  err.Error(),
		})
	}

	user := models.User{}
	if err := user.CreateFromRegisterRequest(request); err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  err.Error(),
		})
	}

	if err := database.GetDB().Model(&models.User{}).Create(&user).Error; err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  err.Error(),
		})
	}

	claims := &jwtCustomClaims{
		user.ID,
		true,
		jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(time.Minute * 30)),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	t, err := token.SignedString([]byte("secret"))
	if err != nil {
		return err
	}

	return c.JSON(http.StatusOK, echo.Map{
		"token": t,
	})
}
