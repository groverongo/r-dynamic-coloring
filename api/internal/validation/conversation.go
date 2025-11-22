package validation

type conversationMessages struct {
	Role    string `json:"role" validate:"required"`
	Content string `json:"content" validate:"required"`
}

type CreateConversationRequest struct {
	GraphId string               `json:"graphId" validate:"required"`
	Message conversationMessages `json:"message" validate:"required"`
}

func (c *CreateConversationRequest) Validate() error {
	return GetValidate().Struct(c)
}

type CreateConversationResponse struct {
	Id string `json:"id" validate:"required"`
}

type ContinueConversationRequest struct {
	Id      string               `json:"id" validate:"required"`
	Message conversationMessages `json:"message" validate:"required"`
}

func (c *ContinueConversationRequest) Validate() error {
	return GetValidate().Struct(c)
}

type ContinueConversationResponse struct {
	Message conversationMessages `json:"message" validate:"required"`
}

type GetConversationResponse struct {
	Id       string                 `json:"id" validate:"required"`
	Messages []conversationMessages `json:"messages" validate:"required"`
}
