package cases

import (
	"context"
	"reflect"

	"github.com/pkg/errors"
	"github.com/printing_house/internal/entities"
)

// UserService handles business logic for users
type UserService struct {
	repo Repository
}

// NewUserService creates a new user service
func NewUserService(repo Repository) (*UserService, error) {
	if repo == nil {
		return nil, entities.ErrInvalidInterface
	}

	val := reflect.ValueOf(repo)
	if val.Kind() == reflect.Ptr && val.IsNil() {
		return nil, entities.ErrInvalidInterface
	}

	return &UserService{repo: repo}, nil
}

// CreateUser creates a new user
func (s *UserService) CreateUser(ctx context.Context, user *entities.User) (*entities.User, error) {
	if user == nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "user cannot be nil")
	}

	// Check if username already exists
	existingUser, err := s.repo.GetUserByUsername(ctx, user.Username)
	if err == nil && existingUser != nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "username already exists")
	}

	// Check if email already exists
	existingUser, err = s.repo.GetUserByEmail(ctx, user.Email)
	if err == nil && existingUser != nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "email already exists")
	}

	return s.repo.CreateUser(ctx, user)
}

// GetUserByID retrieves a user by ID
func (s *UserService) GetUserByID(ctx context.Context, id int) (*entities.User, error) {
	if id <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "user ID must be positive")
	}
	return s.repo.GetUserByID(ctx, id)
}

// GetUserByUsername retrieves a user by username
func (s *UserService) GetUserByUsername(ctx context.Context, username string) (*entities.User, error) {
	if username == "" {
		return nil, errors.Wrap(entities.ErrInvalidInput, "username cannot be empty")
	}
	return s.repo.GetUserByUsername(ctx, username)
}

// GetUserByEmail retrieves a user by email
func (s *UserService) GetUserByEmail(ctx context.Context, email string) (*entities.User, error) {
	if email == "" {
		return nil, errors.Wrap(entities.ErrInvalidInput, "email cannot be empty")
	}
	return s.repo.GetUserByEmail(ctx, email)
}

// GetAllUsers retrieves all users
func (s *UserService) GetAllUsers(ctx context.Context) ([]*entities.User, error) {
	return s.repo.GetAllUsers(ctx)
}

// UpdateUser updates a user
func (s *UserService) UpdateUser(ctx context.Context, user *entities.User) (*entities.User, error) {
	if user == nil {
		return nil, errors.Wrap(entities.ErrInvalidInput, "user cannot be nil")
	}
	if user.ID <= 0 {
		return nil, errors.Wrap(entities.ErrInvalidInput, "user ID must be positive")
	}
	return s.repo.UpdateUser(ctx, user)
}

// DeleteUser deletes a user
func (s *UserService) DeleteUser(ctx context.Context, id int) error {
	if id <= 0 {
		return errors.Wrap(entities.ErrInvalidInput, "user ID must be positive")
	}
	return s.repo.DeleteUser(ctx, id)
}

// AuthenticateUser authenticates a user by username/email and password
func (s *UserService) AuthenticateUser(ctx context.Context, usernameOrEmail string, password string) (*entities.User, error) {
	if usernameOrEmail == "" {
		return nil, errors.Wrap(entities.ErrInvalidInput, "username or email cannot be empty")
	}
	if password == "" {
		return nil, errors.Wrap(entities.ErrInvalidInput, "password cannot be empty")
	}

	// Try to get user by username first
	user, err := s.repo.GetUserByUsername(ctx, usernameOrEmail)
	if err != nil {
		// If not found by username, try by email
		user, err = s.repo.GetUserByEmail(ctx, usernameOrEmail)
		if err != nil {
			return nil, errors.Wrap(entities.ErrNotFound, "invalid credentials")
		}
	}

	// Check if user is active
	if !user.IsActive {
		return nil, errors.Wrap(entities.ErrInvalidInput, "user account is inactive")
	}

	// Verify password
	if !user.CheckPassword(password) {
		return nil, errors.Wrap(entities.ErrInvalidInput, "invalid credentials")
	}

	return user, nil
}
