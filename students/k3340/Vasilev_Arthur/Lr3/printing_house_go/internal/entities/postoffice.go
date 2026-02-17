package entities

import "github.com/pkg/errors"

// PostOffice represents a post office (почтовое отделение)
type PostOffice struct {
	ID      int    `json:"id"`
	Number  string `json:"number"`
	Address string `json:"address"`
}

// NewPostOffice creates a new PostOffice with validation
func NewPostOffice(id int, number string, address string) (*PostOffice, error) {
	if number == "" {
		return nil, errors.Wrap(ErrInvalidField, "PostOffice number is empty")
	}
	if address == "" {
		return nil, errors.Wrap(ErrInvalidField, "PostOffice address is empty")
	}

	return &PostOffice{
		ID:      id,
		Number:  number,
		Address: address,
	}, nil
}
