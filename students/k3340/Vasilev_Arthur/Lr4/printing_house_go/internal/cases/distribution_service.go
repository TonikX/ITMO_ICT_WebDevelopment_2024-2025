package cases

import (
	"context"
	"reflect"

	"github.com/pkg/errors"
	"github.com/printing_house/internal/entities"
)

// DistributionService handles business logic for distributions
type DistributionService struct {
	repo Repository
}

// NewDistributionService creates a new distribution service
func NewDistributionService(repo Repository) (*DistributionService, error) {
	if repo == nil {
		return nil, entities.ErrInvalidInterface
	}

	val := reflect.ValueOf(repo)
	if val.Kind() == reflect.Ptr && val.IsNil() {
		return nil, entities.ErrInvalidInterface
	}

	return &DistributionService{repo: repo}, nil
}

// CreateDistribution creates a new distribution
func (s *DistributionService) CreateDistribution(ctx context.Context, d *entities.Distribution) (*entities.Distribution, error) {
	if d == nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "distribution cannot be nil")
	}
	return s.repo.CreateDistribution(ctx, d)
}

// GetDistributionByID retrieves a distribution by ID
func (s *DistributionService) GetDistributionByID(ctx context.Context, id int) (*entities.Distribution, error) {
	if id <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "distribution ID must be positive")
	}
	return s.repo.GetDistributionByID(ctx, id)
}

// GetAllDistributions retrieves all distributions (by loading all from DB)
func (s *DistributionService) GetAllDistributions(ctx context.Context) ([]*entities.Distribution, error) {
	// This would require another interface method
	postOffices, err := s.repo.GetAllPostOffices(ctx)
	if err != nil {
		return nil, errors.Wrap(err, "failed to get post offices")
	}

	var result []*entities.Distribution
	for _, po := range postOffices {
		if po != nil {
			distributions, err := s.repo.GetDistributionsByPostOfficeID(ctx, po.ID)
			if err == nil {
				result = append(result, distributions...)
			}
		}
	}

	return result, nil
}

// UpdateDistribution updates a distribution
func (s *DistributionService) UpdateDistribution(ctx context.Context, d *entities.Distribution) (*entities.Distribution, error) {
	if d == nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "distribution cannot be nil")
	}
	if d.ID <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "distribution ID must be positive")
	}
	return s.repo.UpdateDistribution(ctx, d)
}

// DeleteDistribution deletes a distribution
func (s *DistributionService) DeleteDistribution(ctx context.Context, id int) error {
	if id <= 0 {
		return errors.Wrap(entities.ErrInvalidInput, "distribution ID must be positive")
	}
	return s.repo.DeleteDistribution(ctx, id)
}

// GetDistributionsByPostOfficeID retrieves distributions for a specific post office
func (s *DistributionService) GetDistributionsByPostOfficeID(ctx context.Context, postOfficeID int) ([]*entities.Distribution, error) {
	if postOfficeID <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "post office ID must be positive")
	}
	return s.repo.GetDistributionsByPostOfficeID(ctx, postOfficeID)
}

// GetDistributionsByNewspaperID retrieves distributions for a specific newspaper
func (s *DistributionService) GetDistributionsByNewspaperID(ctx context.Context, newspaperID int) ([]*entities.Distribution, error) {
	if newspaperID <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "newspaper ID must be positive")
	}
	return s.repo.GetDistributionsByNewspaperID(ctx, newspaperID)
}

// GetDistributionsByPrintingHouseID retrieves distributions for a specific printing house
func (s *DistributionService) GetDistributionsByPrintingHouseID(ctx context.Context, printingHouseID int) ([]*entities.Distribution, error) {
	if printingHouseID <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "printing house ID must be positive")
	}
	return s.repo.GetDistributionsByPrintingHouseID(ctx, printingHouseID)
}
