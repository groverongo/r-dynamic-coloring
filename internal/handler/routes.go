package handler

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

// InitRoutes initializes all routes
func InitRoutes(e *echo.Echo) {
	// Health check endpoint
	e.GET("/health", healthCheck)

	// API v1 group
	api := e.Group("/api/v1")
	{
		api.GET("", apiInfo)
		api.POST("/assign-coloring", AssignColoring)
	}
}

// HealthCheck godoc
// @Summary Show the status of server.
// @Description get the status of server.
// @Tags root
// @Accept */*
// @Produce json
// @Success 200 {object} map[string]interface{}
// @Router /health [get]
func healthCheck(c echo.Context) error {
	return c.JSON(http.StatusOK, map[string]interface{}{
		"status": "OK",
	})
}

// apiInfo returns basic API information
func apiInfo(c echo.Context) error {
	return c.JSON(http.StatusOK, map[string]interface{}{
		"name":    "r-dynamic-coloring-service",
		"version": "0.1.0",
		"docs":    "/swagger/index.html",
	})
}
