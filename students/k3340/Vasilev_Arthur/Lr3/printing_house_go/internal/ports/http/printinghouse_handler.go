package http

import (
	"encoding/json"
	"net/http"

	"github.com/printing_house/internal/entities"
	"github.com/printing_house/pkg/dto"
)

// handleGetAllPrintingHouses GET /printing-houses
func (s *Server) handleGetAllPrintingHouses(w http.ResponseWriter, r *http.Request) {
	houses, err := s.printingHouseService.GetAllPrintingHouses(r.Context())
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to get printing houses")
		return
	}

	result := make([]dto.PrintingHouseDTO, len(houses))
	for i, h := range houses {
		result[i] = dto.PrintingHouseDTO{
			ID:       h.ID,
			Name:     h.Name,
			Address:  h.Address,
			IsActive: h.IsActive,
		}
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleCreatePrintingHouse POST /printing-houses
func (s *Server) handleCreatePrintingHouse(w http.ResponseWriter, r *http.Request) {
	var req dto.CreatePrintingHouseRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	ph, err := entities.NewPrintingHouse(0, req.Name, req.Address, req.IsActive)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, err.Error())
		return
	}

	saved, err := s.printingHouseService.CreatePrintingHouse(r.Context(), ph)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to create printing house")
		return
	}

	result := dto.PrintingHouseDTO{
		ID:       saved.ID,
		Name:     saved.Name,
		Address:  saved.Address,
		IsActive: saved.IsActive,
	}

	s.respondWithJSON(w, http.StatusCreated, result)
}

// handleGetPrintingHouse GET /printing-houses/:id
func (s *Server) handleGetPrintingHouse(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid printing house ID")
		return
	}

	ph, err := s.printingHouseService.GetPrintingHouseByID(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "printing house not found")
		return
	}

	result := dto.PrintingHouseDTO{
		ID:       ph.ID,
		Name:     ph.Name,
		Address:  ph.Address,
		IsActive: ph.IsActive,
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleUpdatePrintingHouse PUT /printing-houses/:id
func (s *Server) handleUpdatePrintingHouse(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid printing house ID")
		return
	}

	var req dto.UpdatePrintingHouseRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	ph, err := s.printingHouseService.GetPrintingHouseByID(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "printing house not found")
		return
	}

	if req.Name != nil {
		ph.Name = *req.Name
	}
	if req.Address != nil {
		ph.Address = *req.Address
	}
	if req.IsActive != nil {
		ph.IsActive = *req.IsActive
	}

	updated, err := s.printingHouseService.UpdatePrintingHouse(r.Context(), ph)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to update printing house")
		return
	}

	result := dto.PrintingHouseDTO{
		ID:       updated.ID,
		Name:     updated.Name,
		Address:  updated.Address,
		IsActive: updated.IsActive,
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleDeletePrintingHouse DELETE /printing-houses/:id
func (s *Server) handleDeletePrintingHouse(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid printing house ID")
		return
	}

	err = s.printingHouseService.DeletePrintingHouse(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to delete printing house")
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

// handleLargestCirculationEditor GET /printing-houses/:id/largest-circulation-editor
func (s *Server) handleLargestCirculationEditor(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid printing house ID")
		return
	}

	run, err := s.printingHouseService.GetLargestCirculationEditor(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "no printing runs found")
		return
	}

	ph, _ := s.printingHouseService.GetPrintingHouseByID(r.Context(), id)

	result := dto.LargestCirculationEditorResponse{
		PrintingHouse:  ph.Name,
		Newspaper:      run.Newspaper.Title,
		Circulation:    run.Circulation,
		EditorLastName: run.Newspaper.EditorLastName,
		EditorFullName: run.Newspaper.EditorFullName(),
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleGetPrintingHouseFullDetail GET /printing-houses/:id/full-detail
func (s *Server) handleGetPrintingHouseFullDetail(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid printing house ID")
		return
	}

	ph, err := s.printingHouseService.GetPrintingHouseByID(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "printing house not found")
		return
	}

	result := dto.PrintingHouseDetailDTO{
		ID:           ph.ID,
		Name:         ph.Name,
		Address:      ph.Address,
		IsActive:     ph.IsActive,
		PrintingRuns: []dto.PrintingRunNestedDTO{},
	}

	// Get printing runs for this printing house
	printingRuns, err := s.printingRunService.GetPrintingRunsByPrintingHouseID(r.Context(), id)
	if err == nil {
		for _, pr := range printingRuns {
			if pr.Newspaper == nil || pr.PrintingHouse == nil {
				continue
			}
			
			result.PrintingRuns = append(result.PrintingRuns, dto.PrintingRunNestedDTO{
				ID:          pr.ID,
				Newspaper:   dto.NewspaperDTO{
					ID:               pr.Newspaper.ID,
					Title:            pr.Newspaper.Title,
					PublicationIndex: pr.Newspaper.PublicationIndex,
					EditorFirstName:  pr.Newspaper.EditorFirstName,
					EditorLastName:   pr.Newspaper.EditorLastName,
					EditorMiddleName: pr.Newspaper.EditorMiddleName,
					EditorFullName:   pr.Newspaper.EditorFullName(),
					PricePerCopy:     pr.Newspaper.PricePerCopy,
				},
				PrintingHouse: dto.PrintingHouseDTO{
					ID:       ph.ID,
					Name:     ph.Name,
					Address:  ph.Address,
					IsActive: ph.IsActive,
				},
				Circulation: pr.Circulation,
			})
		}
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handlePrintingHouseReport GET /printing-houses/report
func (s *Server) handlePrintingHouseReport(w http.ResponseWriter, r *http.Request) {
	houses, err := s.printingHouseService.GetAllPrintingHouses(r.Context())
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to get printing houses")
		return
	}

	var result []dto.PrintingHouseReportResponse
	for _, ph := range houses {
		if !ph.IsActive {
			continue
		}

		phResult := dto.PrintingHouseReportResponse{
			PrintingHouse:   dto.PrintingHouseDTO{ID: ph.ID, Name: ph.Name, Address: ph.Address, IsActive: ph.IsActive},
			TotalNewspapers: 0,
			Newspapers:      []dto.NewspaperReportItemDTO{},
		}

		// Get printing runs for this printing house
		printingRuns, err := s.printingRunService.GetPrintingRunsByPrintingHouseID(r.Context(), ph.ID)
		if err == nil && len(printingRuns) > 0 {
			phResult.TotalNewspapers = len(printingRuns)

			// For each printing run (newspaper), get distributions
			for _, pr := range printingRuns {
				if pr.Newspaper == nil {
					continue
				}
				
				newspaperItem := dto.NewspaperReportItemDTO{
					Newspaper:        pr.Newspaper.Title,
					Circulation:      pr.Circulation,
					Distributions:    []dto.DistributionReportItemDTO{},
					TotalDistributed: 0,
				}

				// Get distributions for this newspaper and printing house
				allDistributions, distErr := s.distributionService.GetAllDistributions(r.Context())
				if distErr == nil {
					totalDistributed := 0
					for _, d := range allDistributions {
						// Match distributions for this newspaper and printing house
						if d.PostOffice != nil && d.NewspaperID == pr.NewspaperID && d.PrintingHouseID == ph.ID {
							newspaperItem.Distributions = append(newspaperItem.Distributions, dto.DistributionReportItemDTO{
								PostOfficeNumber:  d.PostOffice.Number,
								PostOfficeAddress: d.PostOffice.Address,
								Quantity:          d.Quantity,
							})
							totalDistributed += d.Quantity
						}
					}
					newspaperItem.TotalDistributed = totalDistributed
				}

				phResult.Newspapers = append(phResult.Newspapers, newspaperItem)
			}
		}

		result = append(result, phResult)
	}

	s.respondWithJSON(w, http.StatusOK, result)
}
