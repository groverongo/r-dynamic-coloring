package validation

type AskQuestionRequest struct {
	Graph  map[string][]string `json:"graph" validate:"required"`
	Prompt string              `json:"prompt" validate:"required"`
}

func (r *AskQuestionRequest) Validate() error {
	return GetValidate().Struct(r)
}

type AskQuestionResponse struct {
	Answer string `json:"answer"`
}

func (r *AskQuestionResponse) Validate() error {
	return GetValidate().Struct(r)
}
