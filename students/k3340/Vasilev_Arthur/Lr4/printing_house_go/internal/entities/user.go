package entities

import (
	"time"

	"golang.org/x/crypto/bcrypt"
)

// User represents a user in the system
type User struct {
	ID           int       `json:"id"`
	Username     string    `json:"username"`
	Email        string    `json:"email"`
	PasswordHash string    `json:"-"` // Never expose password hash in JSON
	FirstName    *string   `json:"first_name,omitempty"`
	LastName     *string   `json:"last_name,omitempty"`
	IsActive     bool      `json:"is_active"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
}

// NewUser creates a new User with validation and password hashing
func NewUser(
	id int,
	username string,
	email string,
	password string,
	firstName *string,
	lastName *string,
) (*User, error) {
	if username == "" {
		return nil, ErrInvalidField
	}
	if email == "" {
		return nil, ErrInvalidField
	}
	if password == "" {
		return nil, ErrInvalidField
	}

	// Hash password with bcrypt
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}

	now := time.Now()

	return &User{
		ID:           id,
		Username:     username,
		Email:        email,
		PasswordHash: string(hashedPassword),
		FirstName:    firstName,
		LastName:     lastName,
		IsActive:     true,
		CreatedAt:    now,
		UpdatedAt:    now,
	}, nil
}

// CheckPassword verifies if the provided password matches the user's password hash
func (u *User) CheckPassword(password string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(u.PasswordHash), []byte(password))
	return err == nil
}

// FullName returns the full name of the user
func (u *User) FullName() string {
	if u.FirstName != nil && u.LastName != nil {
		return *u.FirstName + " " + *u.LastName
	}
	if u.FirstName != nil {
		return *u.FirstName
	}
	if u.LastName != nil {
		return *u.LastName
	}
	return u.Username
}
