package validation

type AdjacenyList = map[int][]int

type AssignColoringRequest struct {
	Graph  AdjacenyList `json:"graph" validate:"required,min=1,dive,keys,min=0,endkeys,required,min=1,dive,min=0"`
	Method string       `json:"method" validate:"required,oneof=ASR ASR-H ASR-R ASR-RH"`
}

// Validate performs validation on the AdjacenyList
func (a *AssignColoringRequest) Validate() error {
	return GetValidate().Struct(a)
}
