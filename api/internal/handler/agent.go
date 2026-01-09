package handler

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"r-hued-coloring-service/internal/validation"
	"r-hued-coloring-service/pkg/utils"

	"github.com/labstack/echo/v4"
)

func AskQuestion(c echo.Context) error {

	var req validation.AskQuestionRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]interface{}{
			"message": "Invalid request",
			"data":    nil,
		})
	}
	if err := req.Validate(); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]interface{}{
			"message": "Invalid request",
			"data":    nil,
		})
	}

	// Convert request to JSON
	jsonData, err := json.Marshal(req)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  "Failed to marshal request: " + err.Error(),
		})
	}

	// Create a new request with JSON body
	url := fmt.Sprintf("%s/invoke", utils.AGENT_MICROSERVICE_URL)
	resp, err := utils.RequestPostJSONAPIKey(url, jsonData, os.Getenv("C_AGENT_API_KEY"))
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

	if resp.StatusCode != http.StatusOK {
		return c.JSONBlob(resp.StatusCode, body)
	}

	var serviceResponse validation.AskQuestionResponse
	if err := json.Unmarshal(body, &serviceResponse); err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  "Failed to unmarshal response body: " + err.Error(),
		})
	}

	if err := serviceResponse.Validate(); err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  "Failed to validate response body: " + err.Error(),
		})
	}

	return c.JSON(http.StatusOK, serviceResponse)
}
