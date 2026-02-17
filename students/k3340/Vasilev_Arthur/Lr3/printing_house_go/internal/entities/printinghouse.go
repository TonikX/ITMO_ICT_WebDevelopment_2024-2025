package entities

import "github.com/pkg/errors"

// PrintingHouse represents a printing house (типография)
type PrintingHouse struct {
	ID       int    `json:"id"`
	Name     string `json:"name"`
	Address  string `json:"address"`
	IsActive bool   `json:"is_active"`
}

// NewPrintingHouse creates a new PrintingHouse with validation
func NewPrintingHouse(id int, name string, address string, isActive bool) (*PrintingHouse, error) {
	if name == "" {
		return nil, errors.Wrap(ErrInvalidField, "PrintingHouse name is empty")
	}
	if address == "" {
		return nil, errors.Wrap(ErrInvalidField, "PrintingHouse address is empty")
	}

	return &PrintingHouse{
		ID:       id,
		Name:     name,
		Address:  address,
		IsActive: isActive,
	}, nil
}
