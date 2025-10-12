package utils

import "os"

const (
	ACR    = "ACR"
	ACR_H  = "ACR-H"
	ACR_R  = "ACR-R"
	ACR_RH = "ACR-RH"
)

var COLORING_MICROSERVICE_URL string = os.Getenv("COLORING_MICROSERVICE_URL")
