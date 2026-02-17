package http

import (
	"encoding/json"
	"net/http"
	"time"

	"github.com/printing_house/internal/cases"
	"github.com/printing_house/internal/entities"
	"github.com/printing_house/pkg/dto"
)

// handleCreateAPIToken POST /auth/tokens - Create new API token
func (s *Server) handleCreateAPIToken(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Name      string `json:"name"`
		ExpiresIn string `json:"expires_in"` // e.g., "24h", "7d", "30d"
	}

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	if req.Name == "" {
		s.respondWithError(w, http.StatusBadRequest, "name is required")
		return
	}

	// Parse duration - default 24 hours
	duration := 24 * time.Hour
	if req.ExpiresIn != "" {
		parsedDuration, err := time.ParseDuration(req.ExpiresIn)
		if err != nil {
			s.respondWithError(w, http.StatusBadRequest, "invalid expires_in format, use Go duration format (e.g., '24h', '7d')")
			return
		}
		duration = parsedDuration
	}

	// Create token
	token, err := entities.NewAPIToken(req.Name, duration)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, err.Error())
		return
	}

	// Save to database
	savedToken, err := s.tokenService.CreateToken(r.Context(), token)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to create token")
		return
	}

	result := dto.APITokenDTO{
		ID:        savedToken.ID,
		Token:     savedToken.Token,
		Name:      savedToken.Name,
		ExpiresAt: savedToken.ExpiresAt,
		CreatedAt: savedToken.CreatedAt,
		IsActive:  savedToken.IsActive,
	}

	s.respondWithJSON(w, http.StatusCreated, result)
}

// handleGetAPITokens GET /auth/tokens - List all tokens (requires auth)
func (s *Server) handleGetAPITokens(w http.ResponseWriter, r *http.Request) {
	tokens, err := s.tokenService.GetAllTokens(r.Context())
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to get tokens")
		return
	}

	result := make([]dto.APITokenDTO, len(tokens))
	for i, t := range tokens {
		result[i] = dto.APITokenDTO{
			ID:        t.ID,
			Token:     t.Token,
			Name:      t.Name,
			ExpiresAt: t.ExpiresAt,
			CreatedAt: t.CreatedAt,
			IsActive:  t.IsActive,
		}
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleRevokeAPIToken POST /auth/tokens/:token/revoke - Revoke token (requires auth)
func (s *Server) handleRevokeAPIToken(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Token string `json:"token"`
	}

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	if req.Token == "" {
		s.respondWithError(w, http.StatusBadRequest, "token is required")
		return
	}

	err := s.tokenService.RevokeToken(r.Context(), req.Token)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to revoke token")
		return
	}

	s.respondWithJSON(w, http.StatusOK, map[string]string{
		"message": "token revoked successfully",
	})
}

// ============ User Authentication Handlers ============

// handleRegister POST /auth/register - Register new user
func (s *Server) handleRegister(w http.ResponseWriter, r *http.Request) {
	var req dto.RegisterRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	// Validate required fields
	if req.Username == "" {
		s.respondWithError(w, http.StatusBadRequest, "username is required")
		return
	}
	if req.Email == "" {
		s.respondWithError(w, http.StatusBadRequest, "email is required")
		return
	}
	if req.Password == "" {
		s.respondWithError(w, http.StatusBadRequest, "password is required")
		return
	}

	// Create user entity
	user, err := entities.NewUser(0, req.Username, req.Email, req.Password, req.FirstName, req.LastName)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, err.Error())
		return
	}

	// Save user
	savedUser, err := s.userService.CreateUser(r.Context(), user)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	// Generate JWT token (valid for 7 days)
	token, err := cases.GenerateJWTToken(savedUser, 7*24*time.Hour)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to generate token")
		return
	}

	result := dto.LoginResponse{
		Token:     token,
		TokenType: "Bearer",
		ExpiresAt: time.Now().Add(7 * 24 * time.Hour),
		User: dto.UserDTO{
			ID:        savedUser.ID,
			Username:  savedUser.Username,
			Email:     savedUser.Email,
			FirstName: savedUser.FirstName,
			LastName:  savedUser.LastName,
			FullName:  savedUser.FullName(),
			IsActive:  savedUser.IsActive,
			CreatedAt: savedUser.CreatedAt.Format(time.RFC3339),
		},
	}

	s.respondWithJSON(w, http.StatusCreated, result)
}

// handleLogin POST /auth/login - Login user
func (s *Server) handleLogin(w http.ResponseWriter, r *http.Request) {
	var req dto.LoginRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	// Validate required fields
	if req.UsernameOrEmail == "" {
		s.respondWithError(w, http.StatusBadRequest, "username or email is required")
		return
	}
	if req.Password == "" {
		s.respondWithError(w, http.StatusBadRequest, "password is required")
		return
	}

	// Authenticate user
	user, err := s.userService.AuthenticateUser(r.Context(), req.UsernameOrEmail, req.Password)
	if err != nil {
		s.respondWithError(w, http.StatusUnauthorized, "invalid credentials")
		return
	}

	// Generate JWT token (valid for 7 days)
	token, err := cases.GenerateJWTToken(user, 7*24*time.Hour)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to generate token")
		return
	}

	result := dto.LoginResponse{
		Token:     token,
		TokenType: "Bearer",
		ExpiresAt: time.Now().Add(7 * 24 * time.Hour),
		User: dto.UserDTO{
			ID:        user.ID,
			Username:  user.Username,
			Email:     user.Email,
			FirstName: user.FirstName,
			LastName:  user.LastName,
			FullName:  user.FullName(),
			IsActive:  user.IsActive,
			CreatedAt: user.CreatedAt.Format(time.RFC3339),
		},
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleGetCurrentUser GET /auth/me - Get current authenticated user
func (s *Server) handleGetCurrentUser(w http.ResponseWriter, r *http.Request) {
	// Get user ID from context (set by JWT middleware)
	userID, ok := r.Context().Value("user_id").(int)
	if !ok {
		s.respondWithError(w, http.StatusUnauthorized, "user not authenticated")
		return
	}

	user, err := s.userService.GetUserByID(r.Context(), userID)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "user not found")
		return
	}

	result := dto.UserDTO{
		ID:        user.ID,
		Username:  user.Username,
		Email:     user.Email,
		FirstName: user.FirstName,
		LastName:  user.LastName,
		FullName:  user.FullName(),
		IsActive:  user.IsActive,
		CreatedAt: user.CreatedAt.Format(time.RFC3339),
	}

	s.respondWithJSON(w, http.StatusOK, result)
}
