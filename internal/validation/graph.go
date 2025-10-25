package validation

type CreateGraphRequest struct {
	Name               string `json:"name" validate:"required"`
	GraphAdjacencyList string `json:"graphAdjacencyList" validate:"required"`
	VertexGraph        string `json:"vertexGraph" validate:"required"`
	EdgeGraph          string `json:"edgeGraph" validate:"required"`
	LocalColoring      string `json:"localColoring" validate:"required"`
	LocalR             uint   `json:"localR" validate:"required"`
	LocalK             uint   `json:"localK" validate:"required"`
}

// Validate performs validation on the CreateGraphRequest
func (c *CreateGraphRequest) Validate() error {
	return GetValidate().Struct(c)
}

type CreateGraphResponse struct {
	Id string `json:"id"`
}

type GetGraphsResponse struct {
	HasMore bool `json:"hasMore"`
	Graphs  []struct {
		Id        string `json:"id"`
		Name      string `json:"name"`
		CreatedAt string `json:"createdAt"`
		UpdatedAt string `json:"updatedAt"`
	} `json:"graphs"`
}
