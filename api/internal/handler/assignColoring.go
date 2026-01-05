package handler

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
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

	var (
		conversionToInt    map[string]int = make(map[string]int, 0)
		conversionToString map[int]string = make(map[int]string, 0)
	)
	for k := range request.Graph {
		conversionToInt[k] = len(conversionToInt)
		conversionToString[len(conversionToString)] = k
	}
	var isoGraph validation.AdjacenyListService = make(validation.AdjacenyListService, 0)
	for k, v := range request.Graph {
		var neighbors []int
		for _, neighbor := range v {
			neighbors = append(neighbors, conversionToInt[neighbor])
		}
		isoGraph[conversionToInt[k]] = neighbors
	}
	var serviceRequest = validation.AssignColoringServiceRequest{
		GraphType: "adjacency_list",
		Graph:     isoGraph,
		Method:    request.Method,
		K:         request.K,
		R:         request.R,
	}

	// Convert request to JSON
	jsonData, err := json.Marshal(serviceRequest)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"status": "ERROR",
			"error":  "Failed to marshal request: " + err.Error(),
		})
	}

	// Create a new request with JSON body
	url := fmt.Sprintf("%s/color/graph", utils.COLORING_MICROSERVICE_URL)
	client := &http.Client{}
	service, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	service.Header.Set("Content-Type", "application/json")
	service.Header.Set("X-API-Key", os.Getenv("C_MODEL_API_KEY"))
	resp, err := client.Do(service)
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

	var serviceResponse validation.AssignColoringServiceResponse
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

	var response *validation.AssignColoringResponse = validation.NewAssignColoringResponse()
	for k, v := range serviceResponse.Coloring {
		response.Coloring[conversionToString[k]] = v
	}

	return c.JSON(http.StatusOK, *response)
}
