package http

import (
	"encoding/json"
	"net/http"

	"github.com/printing_house/internal/entities"
	"github.com/printing_house/pkg/dto"
)

// handleGetAllDistributions GET /distributions
func (s *Server) handleGetAllDistributions(w http.ResponseWriter, r *http.Request) {
	distributions, err := s.distributionService.GetAllDistributions(r.Context())
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to get distributions")
		return
	}

	result := make([]dto.DistributionDTO, len(distributions))
	for i, d := range distributions {
		result[i] = dto.DistributionDTO{
			ID:              d.ID,
			PostOfficeID:    d.PostOfficeID,
			NewspaperID:     d.NewspaperID,
			PrintingHouseID: d.PrintingHouseID,
			Quantity:        d.Quantity,
		}

		// Add nested data if available
		if d.PostOffice != nil {
			result[i].PostOfficeNumber = d.PostOffice.Number
			result[i].PostOfficeAddress = d.PostOffice.Address
		}
		if d.Newspaper != nil {
			result[i].NewspaperTitle = d.Newspaper.Title
			result[i].NewspaperIndex = d.Newspaper.PublicationIndex
		}
		if d.PrintingHouse != nil {
			result[i].PrintingHouseName = d.PrintingHouse.Name
			result[i].PrintingHouseAddress = d.PrintingHouse.Address
		}
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleCreateDistribution POST /distributions
func (s *Server) handleCreateDistribution(w http.ResponseWriter, r *http.Request) {
	var req dto.CreateDistributionRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	d, err := entities.NewDistribution(0, req.PostOfficeID, req.NewspaperID, req.PrintingHouseID, req.Quantity)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, err.Error())
		return
	}

	saved, err := s.distributionService.CreateDistribution(r.Context(), d)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to create distribution")
		return
	}

	result := dto.DistributionDTO{
		ID:              saved.ID,
		PostOfficeID:    saved.PostOfficeID,
		NewspaperID:     saved.NewspaperID,
		PrintingHouseID: saved.PrintingHouseID,
		Quantity:        saved.Quantity,
	}

	s.respondWithJSON(w, http.StatusCreated, result)
}

// handleGetDistribution GET /distributions/:id
func (s *Server) handleGetDistribution(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid distribution ID")
		return
	}

	d, err := s.distributionService.GetDistributionByID(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "distribution not found")
		return
	}

	result := dto.DistributionDTO{
		ID:              d.ID,
		PostOfficeID:    d.PostOfficeID,
		NewspaperID:     d.NewspaperID,
		PrintingHouseID: d.PrintingHouseID,
		Quantity:        d.Quantity,
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleUpdateDistribution PUT /distributions/:id
func (s *Server) handleUpdateDistribution(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid distribution ID")
		return
	}

	var req dto.UpdateDistributionRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	d, err := s.distributionService.GetDistributionByID(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "distribution not found")
		return
	}

	if req.Quantity != nil {
		d.Quantity = *req.Quantity
	}

	updated, err := s.distributionService.UpdateDistribution(r.Context(), d)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to update distribution")
		return
	}

	result := dto.DistributionDTO{
		ID:              updated.ID,
		PostOfficeID:    updated.PostOfficeID,
		NewspaperID:     updated.NewspaperID,
		PrintingHouseID: updated.PrintingHouseID,
		Quantity:        updated.Quantity,
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleDeleteDistribution DELETE /distributions/:id
func (s *Server) handleDeleteDistribution(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid distribution ID")
		return
	}

	err = s.distributionService.DeleteDistribution(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to delete distribution")
		return
	}

	w.WriteHeader(http.StatusNoContent)
}
