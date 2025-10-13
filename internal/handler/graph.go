package handler

import (
	"net/http"
	"r-hued-coloring-service/internal/database"
	"r-hued-coloring-service/internal/models"
	"r-hued-coloring-service/internal/validation"

	"github.com/labstack/echo/v4"
)

func CreateGraph(c echo.Context) error {

	var request validation.CreateGraphRequest
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

	graph := models.Graph{}
	if err := graph.Create(request); err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  err.Error(),
		})
	}

	if err := database.GetDB().Model(&models.Graph{}).Create(&graph).Error; err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  err.Error(),
		})
	}

	return c.JSON(http.StatusOK, graph)
}
