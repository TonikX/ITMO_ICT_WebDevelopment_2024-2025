package http

import (
	"encoding/json"
	"net/http"
	"reflect"
	"strconv"
	"strings"

	"github.com/go-chi/chi"
	"github.com/printing_house/internal/cases"
	"github.com/printing_house/internal/entities"
	"github.com/printing_house/pkg/dto"
)

// Server represents the HTTP server
type Server struct {
	newspaperService     *cases.NewspaperService
	printingHouseService *cases.PrintingHouseService
	postOfficeService    *cases.PostOfficeService
	distributionService  *cases.DistributionService
	tokenService         *cases.TokenService
	userService          *cases.UserService
	repository           cases.Repository
	router               *chi.Mux
}

// NewServer creates a new HTTP server
func NewServer(
	newspaperService *cases.NewspaperService,
	printingHouseService *cases.PrintingHouseService,
	postOfficeService *cases.PostOfficeService,
	distributionService *cases.DistributionService,
	tokenService *cases.TokenService,
	userService *cases.UserService,
	repository cases.Repository,
) (*Server, error) {
	if newspaperService == nil || printingHouseService == nil || postOfficeService == nil || distributionService == nil || tokenService == nil || userService == nil || repository == nil {
		return nil, entities.ErrInvalidInterface
	}

	val := reflect.ValueOf(newspaperService)
	if val.Kind() == reflect.Ptr && val.IsNil() {
		return nil, entities.ErrInvalidInterface
	}

	s := &Server{
		newspaperService:     newspaperService,
		printingHouseService: printingHouseService,
		postOfficeService:    postOfficeService,
		distributionService:  distributionService,
		tokenService:         tokenService,
		userService:          userService,
		repository:           repository,
	}
	s.router = chi.NewRouter()
	s.setupRoutes()
	return s, nil
}

// ServeHTTP implements http.Handler
func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	s.router.ServeHTTP(w, r)
}

// setupRoutes configures all routes
func (s *Server) setupRoutes() {
	s.router.Route("/api/v1", func(r chi.Router) {
		// ===== AUTH ROUTES =====
		r.Route("/auth", func(r chi.Router) {
			// Public routes (no authentication required)
			r.Post("/register", s.handleRegister) // Register new user
			r.Post("/login", s.handleLogin)       // Login user
			r.Post("/tokens", s.handleCreateAPIToken) // Create new API token

			// Protected routes - with Bearer token
			r.Group(func(r chi.Router) {
				r.Use(BearerTokenMiddleware(s.repository))
				r.Get("/me", s.handleGetCurrentUser)         // Get current user
				r.Get("/tokens", s.handleGetAPITokens)       // List all tokens
				r.Post("/tokens/revoke", s.handleRevokeAPIToken) // Revoke token
			})
		})

		// ===== NEWSPAPER ROUTES =====
		r.Route("/newspapers", func(r chi.Router) {
			// GET endpoints - open
			r.Get("/", s.handleGetAllNewspapers)
			r.Get("/by-name", s.handleGetNewspaperByName)
			r.Get("/info", s.handleGetNewspaperInfo)

			// POST - requires token
			r.Group(func(r chi.Router) {
				r.Use(BearerTokenMiddleware(s.repository))
				r.Post("/", s.handleCreateNewspaper)
			})

			r.Route("/{id}", func(r chi.Router) {
				// GET endpoints - open
				r.Get("/", s.handleGetNewspaper)
				r.Get("/full-detail", s.handleGetNewspaperFullDetail)

				// PUT/DELETE - requires token
				r.Group(func(r chi.Router) {
					r.Use(BearerTokenMiddleware(s.repository))
					r.Put("/", s.handleUpdateNewspaper)
					r.Delete("/", s.handleDeleteNewspaper)
				})
			})
		})

		// ===== PRINTING HOUSE ROUTES =====
		r.Route("/printing-houses", func(r chi.Router) {
			// GET endpoints - open
			r.Get("/", s.handleGetAllPrintingHouses)
			r.Get("/report", s.handlePrintingHouseReport)

			// POST - requires token
			r.Group(func(r chi.Router) {
				r.Use(BearerTokenMiddleware(s.repository))
				r.Post("/", s.handleCreatePrintingHouse)
			})

			r.Route("/{id}", func(r chi.Router) {
				// GET endpoints - open
				r.Get("/", s.handleGetPrintingHouse)
				r.Get("/largest-circulation-editor", s.handleLargestCirculationEditor)
				r.Get("/full-detail", s.handleGetPrintingHouseFullDetail)

				// PUT/DELETE - requires token
				r.Group(func(r chi.Router) {
					r.Use(BearerTokenMiddleware(s.repository))
					r.Put("/", s.handleUpdatePrintingHouse)
					r.Delete("/", s.handleDeletePrintingHouse)
				})
			})
		})

		// ===== POST OFFICE ROUTES =====
		r.Route("/post-offices", func(r chi.Router) {
			// GET endpoints - open
			r.Get("/", s.handleGetAllPostOffices)
			r.Get("/by-price", s.handleGetPostOfficeByPrice)

			// POST - requires token
			r.Group(func(r chi.Router) {
				r.Use(BearerTokenMiddleware(s.repository))
				r.Post("/", s.handleCreatePostOffice)
			})

			r.Route("/{id}", func(r chi.Router) {
				// GET endpoints - open
				r.Get("/", s.handleGetPostOffice)
				r.Get("/full-detail", s.handleGetPostOfficeFullDetail)

				// PUT/DELETE - requires token
				r.Group(func(r chi.Router) {
					r.Use(BearerTokenMiddleware(s.repository))
					r.Put("/", s.handleUpdatePostOffice)
					r.Delete("/", s.handleDeletePostOffice)
				})
			})
		})

		// ===== DISTRIBUTION ROUTES =====
		r.Route("/distributions", func(r chi.Router) {
			// GET endpoints - open
			r.Get("/", s.handleGetAllDistributions)

			// POST - requires token
			r.Group(func(r chi.Router) {
				r.Use(BearerTokenMiddleware(s.repository))
				r.Post("/", s.handleCreateDistribution)
			})

			r.Route("/{id}", func(r chi.Router) {
				// GET endpoints - open
				r.Get("/", s.handleGetDistribution)

				// PUT/DELETE - requires token
				r.Group(func(r chi.Router) {
					r.Use(BearerTokenMiddleware(s.repository))
					r.Put("/", s.handleUpdateDistribution)
					r.Delete("/", s.handleDeleteDistribution)
				})
			})
		})
	})
}

// Helper functions

func (s *Server) respondWithJSON(w http.ResponseWriter, statusCode int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	json.NewEncoder(w).Encode(data)
}

func (s *Server) respondWithError(w http.ResponseWriter, statusCode int, message string) {
	s.respondWithJSON(w, statusCode, dto.ErrorResponse{Error: message})
}

func (s *Server) getIDFromURL(r *http.Request) (int, error) {
	idStr := chi.URLParam(r, "id")
	return strconv.Atoi(idStr)
}

func (s *Server) getQueryParamInt(r *http.Request, paramName string) (int, error) {
	param := r.URL.Query().Get(paramName)
	if param == "" {
		return 0, entities.ErrInvalidInput
	}
	return strconv.Atoi(param)
}

func (s *Server) getQueryParamFloat(r *http.Request, paramName string) (float64, error) {
	param := r.URL.Query().Get(paramName)
	if param == "" {
		return 0, entities.ErrInvalidInput
	}
	return strconv.ParseFloat(param, 64)
}

func parseNewspaperIDsFromQuery(r *http.Request) []int {
	param := r.URL.Query().Get("ids")
	if param == "" {
		return nil
	}

	parts := strings.Split(param, ",")
	var ids []int
	for _, part := range parts {
		if id, err := strconv.Atoi(strings.TrimSpace(part)); err == nil {
			ids = append(ids, id)
		}
	}
	return ids
}
