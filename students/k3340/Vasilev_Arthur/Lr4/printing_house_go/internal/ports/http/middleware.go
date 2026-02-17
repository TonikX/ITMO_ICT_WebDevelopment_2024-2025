package http

import (
	"context"
	"net/http"
	"strings"

	"github.com/printing_house/internal/cases"
)

// BearerTokenMiddleware validates Bearer token (supports both API tokens and JWT)
func BearerTokenMiddleware(repo cases.Repository) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			// Get Authorization header
			authHeader := r.Header.Get("Authorization")
			if authHeader == "" {
				http.Error(w, `{"error": "missing authorization header"}`, http.StatusUnauthorized)
				return
			}

			// Check if it's Bearer token
			parts := strings.SplitN(authHeader, " ", 2)
			if len(parts) != 2 || parts[0] != "Bearer" {
				http.Error(w, `{"error": "invalid authorization format, expected 'Bearer <token>'"}`, http.StatusUnauthorized)
				return
			}

			token := parts[1]

			// Try JWT first
			claims, err := cases.ValidateJWTToken(token)
			if err == nil {
				// Valid JWT token - add user info to context
				ctx := context.WithValue(r.Context(), "user_id", claims.UserID)
				ctx = context.WithValue(ctx, "username", claims.Username)
				next.ServeHTTP(w, r.WithContext(ctx))
				return
			}

			// If JWT validation failed, try API token
			dbToken, err := repo.GetAPITokenByToken(r.Context(), token)
			if err != nil {
				http.Error(w, `{"error": "invalid token"}`, http.StatusUnauthorized)
				return
			}

			// Check if token is valid and not expired
			if !dbToken.IsValid() {
				http.Error(w, `{"error": "token expired or revoked"}`, http.StatusUnauthorized)
				return
			}

			// Call next handler
			next.ServeHTTP(w, r)
		})
	}
}

// OptionalBearerTokenMiddleware - validates token if provided, but doesn't require it
func OptionalBearerTokenMiddleware(repo cases.Repository) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			authHeader := r.Header.Get("Authorization")
			if authHeader != "" {
				parts := strings.SplitN(authHeader, " ", 2)
				if len(parts) == 2 && parts[0] == "Bearer" {
					token := parts[1]

					// Try JWT first
					claims, err := cases.ValidateJWTToken(token)
					if err == nil {
						// Valid JWT token - add user info to context
						ctx := context.WithValue(r.Context(), "user_id", claims.UserID)
						ctx = context.WithValue(ctx, "username", claims.Username)
						next.ServeHTTP(w, r.WithContext(ctx))
						return
					}

					// Try API token
					dbToken, err := repo.GetAPITokenByToken(r.Context(), token)
					if err != nil || !dbToken.IsValid() {
						http.Error(w, `{"error": "invalid or expired token"}`, http.StatusUnauthorized)
						return
					}
				}
			}
			// Continue even if no token
			next.ServeHTTP(w, r)
		})
	}
}

