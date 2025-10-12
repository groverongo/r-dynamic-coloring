package handler

import (
	"log"
	"net/http"
	"r-hued-coloring-service/internal/validation"

	"github.com/labstack/echo/v4"
)

func AssignColoring(c echo.Context) error {

	var request validation.AssignColoringRequest
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

	log.Println(request)

	return c.JSON(http.StatusOK, map[string]interface{}{
		"status": "OK",
	})
}
