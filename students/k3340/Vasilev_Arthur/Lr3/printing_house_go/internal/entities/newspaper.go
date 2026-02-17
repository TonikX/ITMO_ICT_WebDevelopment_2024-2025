package entities

import (
	"fmt"

	"github.com/pkg/errors"
)

// Newspaper represents a newspaper in the system
type Newspaper struct {
	ID               int     `json:"id"`
	Title            string  `json:"title"`
	PublicationIndex string  `json:"publication_index"`
	EditorFirstName  string  `json:"editor_first_name"`
	EditorLastName   string  `json:"editor_last_name"`
	EditorMiddleName *string `json:"editor_middle_name"`
	PricePerCopy     float64 `json:"price_per_copy"`
}

// NewNewspaper creates a new Newspaper with validation
func NewNewspaper(
	id int,
	title string,
	publicationIndex string,
	editorFirstName string,
	editorLastName string,
	editorMiddleName *string,
	pricePerCopy float64,
) (*Newspaper, error) {
	if title == "" {
		return nil, errors.Wrap(ErrInvalidField, "Newspaper title is empty")
	}
	if publicationIndex == "" {
		return nil, errors.Wrap(ErrInvalidField, "Newspaper publication_index is empty")
	}
	if editorFirstName == "" {
		return nil, errors.Wrap(ErrInvalidField, "Newspaper editor_first_name is empty")
	}
	if editorLastName == "" {
		return nil, errors.Wrap(ErrInvalidField, "Newspaper editor_last_name is empty")
	}
	if pricePerCopy < 0 {
		return nil, errors.Wrap(ErrInvalidField, "Newspaper price_per_copy cannot be negative")
	}

	return &Newspaper{
		ID:               id,
		Title:            title,
		PublicationIndex: publicationIndex,
		EditorFirstName:  editorFirstName,
		EditorLastName:   editorLastName,
		EditorMiddleName: editorMiddleName,
		PricePerCopy:     pricePerCopy,
	}, nil
}

// EditorFullName returns the full name of the editor
func (n *Newspaper) EditorFullName() string {
	if n.EditorMiddleName != nil && *n.EditorMiddleName != "" {
		return fmt.Sprintf("%s %s %s", n.EditorLastName, n.EditorFirstName, *n.EditorMiddleName)
	}
	return fmt.Sprintf("%s %s", n.EditorLastName, n.EditorFirstName)
}
