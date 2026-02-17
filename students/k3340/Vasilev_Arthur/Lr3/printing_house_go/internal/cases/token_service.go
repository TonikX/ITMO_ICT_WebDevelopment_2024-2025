package cases

import (
	"context"
	"reflect"

	"github.com/pkg/errors"
	"github.com/printing_house/internal/entities"
)

// TokenService handles API token business logic
type TokenService struct {
	repo Repository
}

// NewTokenService creates a new token service
func NewTokenService(repo Repository) (*TokenService, error) {
	if repo == nil {
		return nil, entities.ErrInvalidInterface
	}

	val := reflect.ValueOf(repo)
	if val.Kind() == reflect.Ptr && val.IsNil() {
		return nil, entities.ErrInvalidInterface
	}

	return &TokenService{repo: repo}, nil
}

// CreateToken creates a new API token
func (s *TokenService) CreateToken(ctx context.Context, token *entities.APIToken) (*entities.APIToken, error) {
	if token == nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "token cannot be nil")
	}
	return s.repo.CreateAPIToken(ctx, token)
}

// GetTokenByString retrieves a token by its string value
func (s *TokenService) GetTokenByString(ctx context.Context, tokenStr string) (*entities.APIToken, error) {
	if tokenStr == "" {
		return nil, errors.Wrap(entities.ErrInvalidInput, "token string cannot be empty")
	}
	return s.repo.GetAPITokenByToken(ctx, tokenStr)
}

// GetAllTokens retrieves all tokens
func (s *TokenService) GetAllTokens(ctx context.Context) ([]*entities.APIToken, error) {
	return s.repo.GetAllAPITokens(ctx)
}

// RevokeToken revokes (deactivates) a token
func (s *TokenService) RevokeToken(ctx context.Context, tokenStr string) error {
	if tokenStr == "" {
		return errors.Wrap(entities.ErrInvalidInput, "token string cannot be empty")
	}
	return s.repo.RevokeAPIToken(ctx, tokenStr)
}

// ValidateToken checks if token is valid and not expired
func (s *TokenService) ValidateToken(ctx context.Context, tokenStr string) (bool, error) {
	token, err := s.GetTokenByString(ctx, tokenStr)
	if err != nil {
		return false, err
	}
	return token.IsValid(), nil
}
