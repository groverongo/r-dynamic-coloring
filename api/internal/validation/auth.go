package validation

type RegisterRequest struct {
	Email          string `json:"email"`
	Password       string `json:"password"`
	RepeatPassword string `json:"repeatPassword"`
}

func (r *RegisterRequest) Validate() error {
	return GetValidate().Struct(r)
}

type LoginRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

func (l *LoginRequest) Validate() error {
	return GetValidate().Struct(l)
}
