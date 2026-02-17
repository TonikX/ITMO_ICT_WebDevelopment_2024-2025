package cases

import (
	"context"
	"reflect"

	"github.com/pkg/errors"
	"github.com/printing_house/internal/entities"
)

// PrintingHouseService handles business logic for printing houses
type PrintingHouseService struct {
	repo Repository
}

// NewPrintingHouseService creates a new printing house service
func NewPrintingHouseService(repo Repository) (*PrintingHouseService, error) {
	if repo == nil {
		return nil, entities.ErrInvalidInterface
	}

	val := reflect.ValueOf(repo)
	if val.Kind() == reflect.Ptr && val.IsNil() {
		return nil, entities.ErrInvalidInterface
	}

	return &PrintingHouseService{repo: repo}, nil
}

// CreatePrintingHouse creates a new printing house
func (s *PrintingHouseService) CreatePrintingHouse(ctx context.Context, ph *entities.PrintingHouse) (*entities.PrintingHouse, error) {
	if ph == nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "printing house cannot be nil")
	}
	return s.repo.CreatePrintingHouse(ctx, ph)
}

// GetPrintingHouseByID retrieves a printing house by ID
func (s *PrintingHouseService) GetPrintingHouseByID(ctx context.Context, id int) (*entities.PrintingHouse, error) {
	if id <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "printing house ID must be positive")
	}
	return s.repo.GetPrintingHouseByID(ctx, id)
}

// GetAllPrintingHouses retrieves all active printing houses
func (s *PrintingHouseService) GetAllPrintingHouses(ctx context.Context) ([]*entities.PrintingHouse, error) {
	return s.repo.GetAllPrintingHouses(ctx)
}

// UpdatePrintingHouse updates a printing house
func (s *PrintingHouseService) UpdatePrintingHouse(ctx context.Context, ph *entities.PrintingHouse) (*entities.PrintingHouse, error) {
	if ph == nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "printing house cannot be nil")
	}
	if ph.ID <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "printing house ID must be positive")
	}
	return s.repo.UpdatePrintingHouse(ctx, ph)
}

// DeletePrintingHouse deletes a printing house
func (s *PrintingHouseService) DeletePrintingHouse(ctx context.Context, id int) error {
	if id <= 0 {
		return errors.Wrap(entities.ErrInvalidInput, "printing house ID must be positive")
	}
	return s.repo.DeletePrintingHouse(ctx, id)
}

// GetLargestCirculationEditor returns the editor of the newspaper with largest circulation in a printing house
func (s *PrintingHouseService) GetLargestCirculationEditor(ctx context.Context, printingHouseID int) (*entities.PrintingRun, error) {
	run, err := s.repo.GetMaxCirculationForPrintingHouse(ctx, printingHouseID)
	if err != nil {
		return nil, errors.Wrap(err, "failed to get max circulation")
	}
	if run == nil {
		return nil, errors.Wrap(entities.ErrNotFound, "no printing runs found for this printing house")
	}
	return run, nil
}

// GetPrintingHouseReport returns a report of printing house operations
func (s *PrintingHouseService) GetPrintingHouseReport(ctx context.Context, printingHouseID int) (*entities.PrintingHouse, error) {
	return s.repo.GetPrintingHouseByID(ctx, printingHouseID)
}
