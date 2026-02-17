package cases

import (
	"fmt"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/pkg/errors"
	"github.com/printing_house/internal/entities"
)

// JWTSecret is the secret key for signing JWT tokens
// In production, this should be loaded from environment variables
var JWTSecret = []byte("your-secret-key-change-in-production")

// JWTClaims represents the claims in a JWT token
type JWTClaims struct {
	UserID   int    `json:"user_id"`
	Username string `json:"username"`
	Email    string `json:"email"`
	jwt.RegisteredClaims
}

// GenerateJWTToken generates a new JWT token for a user
func GenerateJWTToken(user *entities.User, expiresIn time.Duration) (string, error) {
	if user == nil {
		return "", errors.New("user cannot be nil")
	}

	expirationTime := time.Now().Add(expiresIn)

	claims := &JWTClaims{
		UserID:   user.ID,
		Username: user.Username,
		Email:    user.Email,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(expirationTime),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			NotBefore: jwt.NewNumericDate(time.Now()),
			Issuer:    "printing_house",
			Subject:   fmt.Sprintf("user:%d", user.ID),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString(JWTSecret)
	if err != nil {
		return "", errors.Wrap(err, "failed to sign JWT token")
	}

	return tokenString, nil
}

// ValidateJWTToken validates and parses a JWT token
func ValidateJWTToken(tokenString string) (*JWTClaims, error) {
	claims := &JWTClaims{}

	token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
		// Verify signing method
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return JWTSecret, nil
	})

	if err != nil {
		return nil, errors.Wrap(err, "failed to parse JWT token")
	}

	if !token.Valid {
		return nil, errors.New("invalid JWT token")
	}

	return claims, nil
}

// ExtractUserIDFromToken extracts user ID from JWT token
func ExtractUserIDFromToken(tokenString string) (int, error) {
	claims, err := ValidateJWTToken(tokenString)
	if err != nil {
		return 0, err
	}
	return claims.UserID, nil
}
