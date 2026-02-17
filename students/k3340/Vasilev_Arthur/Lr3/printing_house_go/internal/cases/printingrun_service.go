package cases

import (
	"context"
	"reflect"

	"github.com/pkg/errors"
	"github.com/printing_house/internal/entities"
)

// PrintingRunService handles business logic for printing runs
type PrintingRunService struct {
	repo Repository
}

// NewPrintingRunService creates a new printing run service
func NewPrintingRunService(repo Repository) (*PrintingRunService, error) {
	if repo == nil {
		return nil, entities.ErrInvalidInterface
	}

	val := reflect.ValueOf(repo)
	if val.Kind() == reflect.Ptr && val.IsNil() {
		return nil, entities.ErrInvalidInterface
	}

	return &PrintingRunService{repo: repo}, nil
}

// CreatePrintingRun creates a new printing run
func (s *PrintingRunService) CreatePrintingRun(ctx context.Context, pr *entities.PrintingRun) (*entities.PrintingRun, error) {
	if pr == nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "printing run cannot be nil")
	}
	return s.repo.CreatePrintingRun(ctx, pr)
}

// GetPrintingRunByID retrieves a printing run by ID
func (s *PrintingRunService) GetPrintingRunByID(ctx context.Context, id int) (*entities.PrintingRun, error) {
	if id <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "printing run ID must be positive")
	}
	return s.repo.GetPrintingRunByID(ctx, id)
}

// GetAllPrintingRuns retrieves all printing runs
func (s *PrintingRunService) GetAllPrintingRuns(ctx context.Context) ([]*entities.PrintingRun, error) {
	return s.repo.GetAllPrintingRuns(ctx)
}

// GetPrintingRunsByNewspaperID retrieves printing runs for a specific newspaper
func (s *PrintingRunService) GetPrintingRunsByNewspaperID(ctx context.Context, newspaperID int) ([]*entities.PrintingRun, error) {
	if newspaperID <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "newspaper ID must be positive")
	}
	return s.repo.GetPrintingRunsByNewspaperID(ctx, newspaperID)
}

// GetPrintingRunsByPrintingHouseID retrieves printing runs for a specific printing house
func (s *PrintingRunService) GetPrintingRunsByPrintingHouseID(ctx context.Context, printingHouseID int) ([]*entities.PrintingRun, error) {
	if printingHouseID <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "printing house ID must be positive")
	}
	return s.repo.GetPrintingRunsByPrintingHouseID(ctx, printingHouseID)
}

// UpdatePrintingRun updates a printing run
func (s *PrintingRunService) UpdatePrintingRun(ctx context.Context, pr *entities.PrintingRun) (*entities.PrintingRun, error) {
	if pr == nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "printing run cannot be nil")
	}
	if pr.ID <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "printing run ID must be positive")
	}
	return s.repo.UpdatePrintingRun(ctx, pr)
}

// DeletePrintingRun deletes a printing run
func (s *PrintingRunService) DeletePrintingRun(ctx context.Context, id int) error {
	if id <= 0 {
		return errors.Wrap(entities.ErrInvalidInput, "printing run ID must be positive")
	}
	return s.repo.DeletePrintingRun(ctx, id)
}
