package entities

import "errors"

var (
	ErrInvalidField     = errors.New("invalid field")
	ErrInvalidInterface = errors.New("invalid interface")
	ErrNotFound         = errors.New("not found")
	ErrAlreadyExists    = errors.New("already exists")
	ErrInvalidInput     = errors.New("invalid input")
)
