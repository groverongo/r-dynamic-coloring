package handler

import (
	"net/http"
	"r-hued-coloring-service/internal/config"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

// InitRoutes initializes all routes
func InitRoutes(e *echo.Echo) {
	// Health check endpoint
	e.GET("/health", healthCheck)

	// API v1 group
	api := e.Group("/api/v1")
	{
		graph := api.Group("/graphs")
		{
			graph.GET("", GetGraphs)
			graph.GET("/:id", GetGraph)
			graph.POST("", CreateGraph)
		}
		agent := api.Group("/agent")
		agent.Use(middleware.RateLimiterWithConfig(config.RateLimiterConfig))
		{
			agent.POST("", AskQuestion)
		}
		conversation := api.Group("/conversation")
		conversation.Use(middleware.RateLimiterWithConfig(config.RateLimiterConfig))
		{
			conversation.GET("/:id", GetConversation)
			conversation.POST("", CreateConversation)
			conversation.PUT("/:id", ContinueConversation)
			conversation.DELETE("/:id", DeleteConversation)
		}
		auth := api.Group("/auth")
		{
			auth.POST("/register", Register)
			auth.POST("/login", Login)
		}
		api.GET("", apiInfo)
		coloring := api.Group("/coloring")
		coloring.Use(middleware.RateLimiterWithConfig(config.RateLimiterConfig))
		{
			coloring.POST("/linear-program", AssignColoring)
		}
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
