package validation

type AdjacenyList = map[string][]string
type AssignColoringRequest struct {
	Graph  AdjacenyList `json:"graph" validate:"required"`
	Method string       `json:"method" validate:"required,oneof=ACR ACR_H ACR_R ACR_RH"`
	K      int          `json:"k" validate:"required,min=1"`
	R      int          `json:"r" validate:"required,min=1"`
}

func (a *AssignColoringRequest) Validate() error {
	return GetValidate().Struct(a)
}

type AssignColoringResponse struct {
	Coloring map[string]int `json:"coloring"`
}

func NewAssignColoringResponse() *AssignColoringResponse {
	return &AssignColoringResponse{
		Coloring: make(map[string]int, 0),
	}
}

type AdjacenyListService = map[int][]int
type AssignColoringServiceRequest struct {
	GraphType string              `json:"graph_type"`
	Graph     AdjacenyListService `json:"graph"`
	Method    string              `json:"method"`
	K         int                 `json:"k"`
	R         int                 `json:"r"`
}

type AssignColoringServiceResponse struct {
	Coloring map[int]int `json:"coloring" validate:"required"`
}

func (a *AssignColoringServiceResponse) Validate() error {
	return GetValidate().Struct(a)
}
