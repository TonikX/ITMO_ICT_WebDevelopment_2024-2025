package cases

import (
	"context"
	"reflect"

	"github.com/pkg/errors"
	"github.com/printing_house/internal/entities"
)

// PostOfficeService handles business logic for post offices
type PostOfficeService struct {
	repo Repository
}

// NewPostOfficeService creates a new post office service
func NewPostOfficeService(repo Repository) (*PostOfficeService, error) {
	if repo == nil {
		return nil, entities.ErrInvalidInterface
	}

	val := reflect.ValueOf(repo)
	if val.Kind() == reflect.Ptr && val.IsNil() {
		return nil, entities.ErrInvalidInterface
	}

	return &PostOfficeService{repo: repo}, nil
}

// CreatePostOffice creates a new post office
func (s *PostOfficeService) CreatePostOffice(ctx context.Context, po *entities.PostOffice) (*entities.PostOffice, error) {
	if po == nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "post office cannot be nil")
	}
	return s.repo.CreatePostOffice(ctx, po)
}

// GetPostOfficeByID retrieves a post office by ID
func (s *PostOfficeService) GetPostOfficeByID(ctx context.Context, id int) (*entities.PostOffice, error) {
	if id <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "post office ID must be positive")
	}
	return s.repo.GetPostOfficeByID(ctx, id)
}

// GetAllPostOffices retrieves all post offices
func (s *PostOfficeService) GetAllPostOffices(ctx context.Context) ([]*entities.PostOffice, error) {
	return s.repo.GetAllPostOffices(ctx)
}

// UpdatePostOffice updates a post office
func (s *PostOfficeService) UpdatePostOffice(ctx context.Context, po *entities.PostOffice) (*entities.PostOffice, error) {
	if po == nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "post office cannot be nil")
	}
	if po.ID <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "post office ID must be positive")
	}
	return s.repo.UpdatePostOffice(ctx, po)
}

// DeletePostOffice deletes a post office
func (s *PostOfficeService) DeletePostOffice(ctx context.Context, id int) error {
	if id <= 0 {
		return errors.Wrap(entities.ErrInvalidInput, "post office ID must be positive")
	}
	return s.repo.DeletePostOffice(ctx, id)
}

// GetPostOfficesByNewspaperPrice returns post offices that receive newspapers with price greater than minPrice
func (s *PostOfficeService) GetPostOfficesByNewspaperPrice(ctx context.Context, minPrice float64) ([]*entities.PostOffice, error) {
	if minPrice < 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "minimum price cannot be negative")
	}
	return s.repo.GetPostOfficesByNewspaperPrice(ctx, minPrice)
}
