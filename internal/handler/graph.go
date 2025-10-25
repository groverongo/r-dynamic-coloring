package handler

import (
	"net/http"
	"r-hued-coloring-service/internal/database"
	"r-hued-coloring-service/internal/models"
	"r-hued-coloring-service/internal/validation"

	"github.com/labstack/echo/v4"
)

func GetGraph(c echo.Context) error {
	id := c.Param("id")
	graph := models.Graph{}
	if err := database.GetDB().Model(&models.Graph{}).Where("id = ?", id).Find(&graph).Error; err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  err.Error(),
		})
	}
	return c.JSON(http.StatusOK, graph)
}

func GetGraphs(c echo.Context) error {
	graphs := []models.Graph{}
	if err := database.GetDB().Model(&models.Graph{}).Select("id", "name", "created_at", "updated_at").Find(&graphs).Error; err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  err.Error(),
		})
	}
	return c.JSON(http.StatusOK, graphs)
}

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

	return c.JSON(http.StatusOK, validation.CreateGraphResponse{Id: graph.ID})
}
