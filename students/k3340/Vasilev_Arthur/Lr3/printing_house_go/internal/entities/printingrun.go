package entities

import "github.com/pkg/errors"

// PrintingRun represents a printing run (тираж) - connection between PrintingHouse and Newspaper
type PrintingRun struct {
	ID              int    `json:"id"`
	PrintingHouseID int    `json:"printing_house_id"`
	NewspaperID     int    `json:"newspaper_id"`
	Circulation     int    `json:"circulation"`
	PrintingHouse   *PrintingHouse `json:"printing_house,omitempty"`
	Newspaper       *Newspaper     `json:"newspaper,omitempty"`
}

// NewPrintingRun creates a new PrintingRun with validation
func NewPrintingRun(id int, printingHouseID int, newspaperID int, circulation int) (*PrintingRun, error) {
	if printingHouseID <= 0 {
		return nil, errors.Wrap(ErrInvalidField, "PrintingRun printing_house_id is invalid")
	}
	if newspaperID <= 0 {
		return nil, errors.Wrap(ErrInvalidField, "PrintingRun newspaper_id is invalid")
	}
	if circulation <= 0 {
		return nil, errors.Wrap(ErrInvalidField, "PrintingRun circulation must be positive")
	}

	return &PrintingRun{
		ID:              id,
		PrintingHouseID: printingHouseID,
		NewspaperID:     newspaperID,
		Circulation:     circulation,
	}, nil
}
