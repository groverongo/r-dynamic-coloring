package handler

import (
	"net/http"
	"r-hued-coloring-service/internal/database"
	"r-hued-coloring-service/internal/models"

	"github.com/labstack/echo/v4"
)

// GetConversation handles GET /conversation/:id
func GetConversation(c echo.Context) error {
	id := c.Param("id")
	conversation := models.Conversation{}
	if err := database.GetDB().Model(&models.Conversation{}).Where("id = ?", id).Find(&conversation).Error; err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  err.Error(),
		})
	}
	return c.JSON(http.StatusOK, conversation)
}

// CreateConversation handles POST /conversation
func CreateConversation(c echo.Context) error {

	return c.JSON(http.StatusCreated, map[string]interface{}{
		"message": "Conversation created",
		"data":    nil,
	})
}

// UpdateConversation handles PUT /conversation/:id
func ContinueConversation(c echo.Context) error {
	id := c.Param("id")
	return c.JSON(http.StatusOK, map[string]interface{}{
		"message": "Conversation updated with ID: " + id,
		"data":    nil,
	})
}

// DeleteConversation handles DELETE /conversation/:id
func DeleteConversation(c echo.Context) error {
	id := c.Param("id")
	return c.JSON(http.StatusOK, map[string]interface{}{
		"message": "Conversation deleted with ID: " + id,
		"data":    nil,
	})
}
