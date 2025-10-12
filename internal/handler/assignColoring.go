package handler

import (
	"bytes"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"r-hued-coloring-service/internal/validation"
	"r-hued-coloring-service/pkg/utils"

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

	// Convert request to JSON
	jsonData, err := json.Marshal(request)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  "Failed to marshal request: " + err.Error(),
		})
	}

	// Create a new request with JSON body
	resp, err := http.Post(utils.COLORING_MICROSERVICE_URL, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  "Failed to send request: " + err.Error(),
		})
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  "Failed to read response body: " + err.Error(),
		})
	}
	log.Println(string(body))

	return c.JSONBlob(http.StatusOK, body)
}
