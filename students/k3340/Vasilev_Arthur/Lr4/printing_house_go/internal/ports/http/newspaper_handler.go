package http

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/printing_house/internal/entities"
	"github.com/printing_house/pkg/dto"
)

// handleGetAllNewspapers GET /newspapers
func (s *Server) handleGetAllNewspapers(w http.ResponseWriter, r *http.Request) {
	newspapers, err := s.newspaperService.GetAllNewspapers(r.Context())
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to get newspapers")
		return
	}

	result := make([]dto.NewspaperDTO, len(newspapers))
	for i, n := range newspapers {
		result[i] = dto.NewspaperDTO{
			ID:               n.ID,
			Title:            n.Title,
			PublicationIndex: n.PublicationIndex,
			EditorFirstName:  n.EditorFirstName,
			EditorLastName:   n.EditorLastName,
			EditorMiddleName: n.EditorMiddleName,
			EditorFullName:   n.EditorFullName(),
			PricePerCopy:     n.PricePerCopy,
		}
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleCreateNewspaper POST /newspapers
func (s *Server) handleCreateNewspaper(w http.ResponseWriter, r *http.Request) {
	var req dto.CreateNewspaperRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	n, err := entities.NewNewspaper(0, req.Title, req.PublicationIndex, req.EditorFirstName, req.EditorLastName, req.EditorMiddleName, req.PricePerCopy)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, err.Error())
		return
	}

	saved, err := s.newspaperService.CreateNewspaper(r.Context(), n)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to create newspaper")
		return
	}

	result := dto.NewspaperDTO{
		ID:               saved.ID,
		Title:            saved.Title,
		PublicationIndex: saved.PublicationIndex,
		EditorFirstName:  saved.EditorFirstName,
		EditorLastName:   saved.EditorLastName,
		EditorMiddleName: saved.EditorMiddleName,
		EditorFullName:   saved.EditorFullName(),
		PricePerCopy:     saved.PricePerCopy,
	}

	s.respondWithJSON(w, http.StatusCreated, result)
}

// handleGetNewspaper GET /newspapers/:id
func (s *Server) handleGetNewspaper(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid newspaper ID")
		return
	}

	n, err := s.newspaperService.GetNewspaperByID(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "newspaper not found")
		return
	}

	result := dto.NewspaperDTO{
		ID:               n.ID,
		Title:            n.Title,
		PublicationIndex: n.PublicationIndex,
		EditorFirstName:  n.EditorFirstName,
		EditorLastName:   n.EditorLastName,
		EditorMiddleName: n.EditorMiddleName,
		EditorFullName:   n.EditorFullName(),
		PricePerCopy:     n.PricePerCopy,
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleUpdateNewspaper PUT /newspapers/:id
func (s *Server) handleUpdateNewspaper(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid newspaper ID")
		return
	}

	var req dto.UpdateNewspaperRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	// Get existing newspaper
	n, err := s.newspaperService.GetNewspaperByID(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "newspaper not found")
		return
	}

	// Update fields
	if req.Title != nil {
		n.Title = *req.Title
	}
	if req.PublicationIndex != nil {
		n.PublicationIndex = *req.PublicationIndex
	}
	if req.EditorFirstName != nil {
		n.EditorFirstName = *req.EditorFirstName
	}
	if req.EditorLastName != nil {
		n.EditorLastName = *req.EditorLastName
	}
	if req.EditorMiddleName != nil {
		n.EditorMiddleName = req.EditorMiddleName
	}
	if req.PricePerCopy != nil {
		n.PricePerCopy = *req.PricePerCopy
	}

	updated, err := s.newspaperService.UpdateNewspaper(r.Context(), n)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to update newspaper")
		return
	}

	result := dto.NewspaperDTO{
		ID:               updated.ID,
		Title:            updated.Title,
		PublicationIndex: updated.PublicationIndex,
		EditorFirstName:  updated.EditorFirstName,
		EditorLastName:   updated.EditorLastName,
		EditorMiddleName: updated.EditorMiddleName,
		EditorFullName:   updated.EditorFullName(),
		PricePerCopy:     updated.PricePerCopy,
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleDeleteNewspaper DELETE /newspapers/:id
func (s *Server) handleDeleteNewspaper(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid newspaper ID")
		return
	}

	err = s.newspaperService.DeleteNewspaper(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to delete newspaper")
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

// handleGetNewspaperByName GET /newspapers/by-name?name=xxx
func (s *Server) handleGetNewspaperByName(w http.ResponseWriter, r *http.Request) {
	name := r.URL.Query().Get("name")
	if name == "" {
		s.respondWithError(w, http.StatusBadRequest, "name parameter is required")
		return
	}

	newspapers, err := s.newspaperService.GetNewspapersByName(r.Context(), name)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "newspapers not found")
		return
	}

	// Get printing runs for each newspaper
	type printingAddressDTO struct {
		PrintingHouse string `json:"printing_house"`
		Address       string `json:"address"`
		Circulation   int    `json:"circulation"`
	}

	type responseDTO struct {
		Newspaper         dto.NewspaperDTO     `json:"newspaper"`
		PrintingAddresses []printingAddressDTO `json:"printing_addresses"`
	}

	var result []responseDTO
	for _, n := range newspapers {
		// Get printing runs for this newspaper to find printing addresses
		addresses := []printingAddressDTO{}
		// NOTE: This requires additional repository method to get printing runs with house info
		// For now, returning empty addresses list

		result = append(result, responseDTO{
			Newspaper: dto.NewspaperDTO{
				ID:               n.ID,
				Title:            n.Title,
				PublicationIndex: n.PublicationIndex,
				EditorFirstName:  n.EditorFirstName,
				EditorLastName:   n.EditorLastName,
				EditorMiddleName: n.EditorMiddleName,
				EditorFullName:   n.EditorFullName(),
				PricePerCopy:     n.PricePerCopy,
			},
			PrintingAddresses: addresses,
		})
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleGetNewspaperInfo GET /newspapers/info?id=xxx or /newspapers/info?name=xxx
func (s *Server) handleGetNewspaperInfo(w http.ResponseWriter, r *http.Request) {
	newspaperID := r.URL.Query().Get("id")
	newspaperName := r.URL.Query().Get("name")

	if newspaperID == "" && newspaperName == "" {
		s.respondWithError(w, http.StatusBadRequest, "id or name parameter is required")
		return
	}

	var n *entities.Newspaper
	var err error

	if newspaperID != "" {
		id, parseErr := strconv.Atoi(newspaperID)
		if parseErr != nil {
			s.respondWithError(w, http.StatusBadRequest, "invalid newspaper ID")
			return
		}
		n, err = s.newspaperService.GetNewspaperByID(r.Context(), id)
	} else {
		n, err = s.newspaperService.GetNewspaperByTitle(r.Context(), newspaperName)
	}

	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "newspaper not found")
		return
	}

	result := dto.NewspaperInfoDTO{
		Title:            n.Title,
		PublicationIndex: n.PublicationIndex,
		PricePerCopy:     n.PricePerCopy,
		Editor:           n.EditorFullName(),
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleGetNewspaperFullDetail GET /newspapers/:id/full-detail
func (s *Server) handleGetNewspaperFullDetail(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid newspaper ID")
		return
	}

	n, err := s.newspaperService.GetNewspaperByID(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "newspaper not found")
		return
	}

	// Get printing runs and distributions
	// This would require methods in the repository to get these relationships
	result := dto.NewspaperDetailDTO{
		ID:               n.ID,
		Title:            n.Title,
		PublicationIndex: n.PublicationIndex,
		EditorFirstName:  n.EditorFirstName,
		EditorLastName:   n.EditorLastName,
		EditorMiddleName: n.EditorMiddleName,
		EditorFullName:   n.EditorFullName(),
		PricePerCopy:     n.PricePerCopy,
		PrintingRuns:     []dto.PrintingRunNestedDTO{},
		Distributions:    []dto.DistributionNestedDTO{},
	}

	s.respondWithJSON(w, http.StatusOK, result)
}
