package entities

import (
	"crypto/rand"
	"encoding/hex"
	"time"
)

// APIToken represents an API authentication token
type APIToken struct {
	ID        int       `json:"id"`
	Token     string    `json:"token"`
	Name      string    `json:"name"`
	ExpiresAt time.Time `json:"expires_at"`
	CreatedAt time.Time `json:"created_at"`
	IsActive  bool      `json:"is_active"`
}

// NewAPIToken creates a new API token with validation
func NewAPIToken(name string, expiresIn time.Duration) (*APIToken, error) {
	if name == "" {
		return nil, ErrInvalidField
	}

	// Generate random token (32 bytes = 64 hex characters)
	tokenBytes := make([]byte, 32)
	if _, err := rand.Read(tokenBytes); err != nil {
		return nil, err
	}

	token := hex.EncodeToString(tokenBytes)
	now := time.Now()
	expiresAt := now.Add(expiresIn)

	return &APIToken{
		Token:     token,
		Name:      name,
		ExpiresAt: expiresAt,
		CreatedAt: now,
		IsActive:  true,
	}, nil
}

// IsExpired checks if token has expired
func (t *APIToken) IsExpired() bool {
	return time.Now().After(t.ExpiresAt)
}

// IsValid checks if token is valid and not expired
func (t *APIToken) IsValid() bool {
	return t.IsActive && !t.IsExpired()
}
