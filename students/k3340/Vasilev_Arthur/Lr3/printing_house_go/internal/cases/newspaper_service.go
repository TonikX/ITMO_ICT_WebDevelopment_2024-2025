package cases

import (
	"context"
	"reflect"

	"github.com/pkg/errors"
	"github.com/printing_house/internal/entities"
)

// NewspaperService handles business logic for newspapers
type NewspaperService struct {
	repo Repository
}

// NewNewspaperService creates a new newspaper service
func NewNewspaperService(repo Repository) (*NewspaperService, error) {
	if repo == nil {
		return nil, entities.ErrInvalidInterface
	}

	val := reflect.ValueOf(repo)
	if val.Kind() == reflect.Ptr && val.IsNil() {
		return nil, entities.ErrInvalidInterface
	}

	return &NewspaperService{repo: repo}, nil
}

// CreateNewspaper creates a new newspaper
func (s *NewspaperService) CreateNewspaper(ctx context.Context, n *entities.Newspaper) (*entities.Newspaper, error) {
	if n == nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "newspaper cannot be nil")
	}
	return s.repo.CreateNewspaper(ctx, n)
}

// GetNewspaperByID retrieves a newspaper by ID
func (s *NewspaperService) GetNewspaperByID(ctx context.Context, id int) (*entities.Newspaper, error) {
	if id <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "newspaper ID must be positive")
	}
	return s.repo.GetNewspaperByID(ctx, id)
}

// GetNewspaperByTitle retrieves a newspaper by title
func (s *NewspaperService) GetNewspaperByTitle(ctx context.Context, title string) (*entities.Newspaper, error) {
	if title == "" {
		return nil, errors.Wrap(entities.ErrInvalidInput, "newspaper title cannot be empty")
	}
	return s.repo.GetNewspaperByTitle(ctx, title)
}

// GetAllNewspapers retrieves all newspapers
func (s *NewspaperService) GetAllNewspapers(ctx context.Context) ([]*entities.Newspaper, error) {
	return s.repo.GetAllNewspapers(ctx)
}

// UpdateNewspaper updates a newspaper
func (s *NewspaperService) UpdateNewspaper(ctx context.Context, n *entities.Newspaper) (*entities.Newspaper, error) {
	if n == nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "newspaper cannot be nil")
	}
	if n.ID <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "newspaper ID must be positive")
	}
	return s.repo.UpdateNewspaper(ctx, n)
}

// DeleteNewspaper deletes a newspaper
func (s *NewspaperService) DeleteNewspaper(ctx context.Context, id int) error {
	if id <= 0 {
		return errors.Wrap(entities.ErrInvalidInput, "newspaper ID must be positive")
	}
	return s.repo.DeleteNewspaper(ctx, id)
}

// GetNewspapersByName retrieves newspapers by name (partial match)
func (s *NewspaperService) GetNewspapersByName(ctx context.Context, name string) ([]*entities.Newspaper, error) {
	if name == "" {
		return nil, errors.Wrap(entities.ErrInvalidInput, "newspaper name cannot be empty")
	}
	newspapers, err := s.repo.GetAllNewspapers(ctx)
	if err != nil {
		return nil, errors.Wrap(err, "failed to get newspapers")
	}

	var result []*entities.Newspaper
	for _, n := range newspapers {
		if n != nil && containsSubstring(n.Title, name) {
			result = append(result, n)
		}
	}

	if len(result) == 0 {
		return nil, errors.Wrap(entities.ErrNotFound, "no newspapers found")
	}

	return result, nil
}

// Helper function
func containsSubstring(str, substr string) bool {
	n := len(substr)
	if n == 0 {
		return true
	}
	for i := 0; i <= len(str)-n; i++ {
		if str[i:i+n] == substr {
			return true
		}
	}
	return false
}
