package dto

import "time"

// ===== User DTOs =====

// UserDTO represents user data transfer object
type UserDTO struct {
	ID        int     `json:"id"`
	Username  string  `json:"username"`
	Email     string  `json:"email"`
	FirstName *string `json:"first_name,omitempty"`
	LastName  *string `json:"last_name,omitempty"`
	FullName  string  `json:"full_name"`
	IsActive  bool    `json:"is_active"`
	CreatedAt string  `json:"created_at"`
}

// RegisterRequest represents registration request
type RegisterRequest struct {
	Username  string  `json:"username"`
	Email     string  `json:"email"`
	Password  string  `json:"password"`
	FirstName *string `json:"first_name,omitempty"`
	LastName  *string `json:"last_name,omitempty"`
}

// LoginRequest represents login request
type LoginRequest struct {
	UsernameOrEmail string `json:"username_or_email"`
	Password        string `json:"password"`
}

// LoginResponse represents login response with JWT token
type LoginResponse struct {
	Token     string    `json:"token"`
	TokenType string    `json:"token_type"`
	ExpiresAt time.Time `json:"expires_at"`
	User      UserDTO   `json:"user"`
}

// UpdateUserRequest represents update user request
type UpdateUserRequest struct {
	Email     *string `json:"email,omitempty"`
	FirstName *string `json:"first_name,omitempty"`
	LastName  *string `json:"last_name,omitempty"`
}
