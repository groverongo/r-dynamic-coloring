package validation

type CreateGraphRequest struct {
	Name          string `json:"name" validate:"required"`
	AdjacencyList string `json:"adjacencyList" validate:"required"`
	DisplayList   string `json:"displayList" validate:"required"`
}

// Validate performs validation on the CreateGraphRequest
func (c *CreateGraphRequest) Validate() error {
	return GetValidate().Struct(c)
}
