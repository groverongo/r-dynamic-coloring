package utils

import (
	"bytes"
	"net/http"
)

func RequestPostJSONAPIKey(url string, jsonData []byte, apiKey string) (*http.Response, error) {
	client := &http.Client{}
	service, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, err
	}
	service.Header.Set("Content-Type", "application/json")
	service.Header.Set("X-API-Key", apiKey)
	return client.Do(service)
}
