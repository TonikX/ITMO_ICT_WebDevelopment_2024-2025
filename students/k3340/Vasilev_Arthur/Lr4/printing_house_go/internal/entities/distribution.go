package entities

import "github.com/pkg/errors"

// Distribution represents distribution of newspapers to post offices (распределение)
type Distribution struct {
	ID              int    `json:"id"`
	PostOfficeID    int    `json:"post_office_id"`
	NewspaperID     int    `json:"newspaper_id"`
	PrintingHouseID int    `json:"printing_house_id"`
	Quantity        int    `json:"quantity"`
	PostOffice      *PostOffice    `json:"post_office,omitempty"`
	Newspaper       *Newspaper     `json:"newspaper,omitempty"`
	PrintingHouse   *PrintingHouse `json:"printing_house,omitempty"`
}

// NewDistribution creates a new Distribution with validation
func NewDistribution(
	id int,
	postOfficeID int,
	newspaperID int,
	printingHouseID int,
	quantity int,
) (*Distribution, error) {
	if postOfficeID <= 0 {
		return nil, errors.Wrap(ErrInvalidField, "Distribution post_office_id is invalid")
	}
	if newspaperID <= 0 {
		return nil, errors.Wrap(ErrInvalidField, "Distribution newspaper_id is invalid")
	}
	if printingHouseID <= 0 {
		return nil, errors.Wrap(ErrInvalidField, "Distribution printing_house_id is invalid")
	}
	if quantity <= 0 {
		return nil, errors.Wrap(ErrInvalidField, "Distribution quantity must be positive")
	}

	return &Distribution{
		ID:              id,
		PostOfficeID:    postOfficeID,
		NewspaperID:     newspaperID,
		PrintingHouseID: printingHouseID,
		Quantity:        quantity,
	}, nil
}
