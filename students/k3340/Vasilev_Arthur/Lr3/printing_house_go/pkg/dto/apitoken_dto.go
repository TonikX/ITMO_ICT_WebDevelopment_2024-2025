package dto

import "time"

// APITokenDTO represents API token data transfer object
type APITokenDTO struct {
	ID        int       `json:"id"`
	Token     string    `json:"token"`
	Name      string    `json:"name"`
	ExpiresAt time.Time `json:"expires_at"`
	CreatedAt time.Time `json:"created_at"`
	IsActive  bool      `json:"is_active"`
}
