package http

import (
	"encoding/json"
	"net/http"

	"github.com/printing_house/internal/entities"
	"github.com/printing_house/pkg/dto"
)

// handleGetAllPrintingRuns GET /printing-runs
func (s *Server) handleGetAllPrintingRuns(w http.ResponseWriter, r *http.Request) {
	runs, err := s.printingRunService.GetAllPrintingRuns(r.Context())
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to get printing runs")
		return
	}

	result := make([]dto.PrintingRunDTO, len(runs))
	for i, pr := range runs {
		result[i] = dto.PrintingRunDTO{
			ID:              pr.ID,
			PrintingHouseID: pr.PrintingHouseID,
			NewspaperID:     pr.NewspaperID,
			Circulation:     pr.Circulation,
		}

		// Add nested data if available
		if pr.PrintingHouse != nil {
			result[i].PrintingHouseName = pr.PrintingHouse.Name
			result[i].PrintingHouseAddress = pr.PrintingHouse.Address
		}
		if pr.Newspaper != nil {
			result[i].NewspaperTitle = pr.Newspaper.Title
			result[i].NewspaperIndex = pr.Newspaper.PublicationIndex
		}
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleCreatePrintingRun POST /printing-runs
func (s *Server) handleCreatePrintingRun(w http.ResponseWriter, r *http.Request) {
	var req dto.CreatePrintingRunRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	pr, err := entities.NewPrintingRun(0, req.PrintingHouseID, req.NewspaperID, req.Circulation)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, err.Error())
		return
	}

	saved, err := s.printingRunService.CreatePrintingRun(r.Context(), pr)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to create printing run")
		return
	}

	result := dto.PrintingRunDTO{
		ID:              saved.ID,
		PrintingHouseID: saved.PrintingHouseID,
		NewspaperID:     saved.NewspaperID,
		Circulation:     saved.Circulation,
	}

	s.respondWithJSON(w, http.StatusCreated, result)
}

// handleGetPrintingRun GET /printing-runs/:id
func (s *Server) handleGetPrintingRun(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid printing run ID")
		return
	}

	pr, err := s.printingRunService.GetPrintingRunByID(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "printing run not found")
		return
	}

	result := dto.PrintingRunDTO{
		ID:              pr.ID,
		PrintingHouseID: pr.PrintingHouseID,
		NewspaperID:     pr.NewspaperID,
		Circulation:     pr.Circulation,
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleUpdatePrintingRun PUT /printing-runs/:id
func (s *Server) handleUpdatePrintingRun(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid printing run ID")
		return
	}

	var req dto.UpdatePrintingRunRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	pr, err := s.printingRunService.GetPrintingRunByID(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "printing run not found")
		return
	}

	if req.Circulation != nil {
		pr.Circulation = *req.Circulation
	}

	updated, err := s.printingRunService.UpdatePrintingRun(r.Context(), pr)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to update printing run")
		return
	}

	result := dto.PrintingRunDTO{
		ID:              updated.ID,
		PrintingHouseID: updated.PrintingHouseID,
		NewspaperID:     updated.NewspaperID,
		Circulation:     updated.Circulation,
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleDeletePrintingRun DELETE /printing-runs/:id
func (s *Server) handleDeletePrintingRun(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid printing run ID")
		return
	}

	err = s.printingRunService.DeletePrintingRun(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to delete printing run")
		return
	}

	w.WriteHeader(http.StatusNoContent)
}
