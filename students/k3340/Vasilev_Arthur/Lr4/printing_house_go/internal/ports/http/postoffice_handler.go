package http

import (
	"encoding/json"
	"net/http"

	"github.com/printing_house/internal/entities"
	"github.com/printing_house/pkg/dto"
)

// handleGetAllPostOffices GET /post-offices
func (s *Server) handleGetAllPostOffices(w http.ResponseWriter, r *http.Request) {
	offices, err := s.postOfficeService.GetAllPostOffices(r.Context())
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to get post offices")
		return
	}

	result := make([]dto.PostOfficeDTO, len(offices))
	for i, po := range offices {
		result[i] = dto.PostOfficeDTO{
			ID:      po.ID,
			Number:  po.Number,
			Address: po.Address,
		}
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleCreatePostOffice POST /post-offices
func (s *Server) handleCreatePostOffice(w http.ResponseWriter, r *http.Request) {
	var req dto.CreatePostOfficeRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	po, err := entities.NewPostOffice(0, req.Number, req.Address)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, err.Error())
		return
	}

	saved, err := s.postOfficeService.CreatePostOffice(r.Context(), po)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to create post office")
		return
	}

	result := dto.PostOfficeDTO{
		ID:      saved.ID,
		Number:  saved.Number,
		Address: saved.Address,
	}

	s.respondWithJSON(w, http.StatusCreated, result)
}

// handleGetPostOffice GET /post-offices/:id
func (s *Server) handleGetPostOffice(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid post office ID")
		return
	}

	po, err := s.postOfficeService.GetPostOfficeByID(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "post office not found")
		return
	}

	result := dto.PostOfficeDTO{
		ID:      po.ID,
		Number:  po.Number,
		Address: po.Address,
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleUpdatePostOffice PUT /post-offices/:id
func (s *Server) handleUpdatePostOffice(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid post office ID")
		return
	}

	var req dto.UpdatePostOfficeRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	po, err := s.postOfficeService.GetPostOfficeByID(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "post office not found")
		return
	}

	if req.Number != nil {
		po.Number = *req.Number
	}
	if req.Address != nil {
		po.Address = *req.Address
	}

	updated, err := s.postOfficeService.UpdatePostOffice(r.Context(), po)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to update post office")
		return
	}

	result := dto.PostOfficeDTO{
		ID:      updated.ID,
		Number:  updated.Number,
		Address: updated.Address,
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleDeletePostOffice DELETE /post-offices/:id
func (s *Server) handleDeletePostOffice(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid post office ID")
		return
	}

	err = s.postOfficeService.DeletePostOffice(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to delete post office")
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

// handleGetPostOfficeByPrice GET /post-offices/by-price?min_price=xxx
func (s *Server) handleGetPostOfficeByPrice(w http.ResponseWriter, r *http.Request) {
	minPrice, err := s.getQueryParamFloat(r, "min_price")
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "min_price parameter is required and must be a number")
		return
	}

	offices, err := s.postOfficeService.GetPostOfficesByNewspaperPrice(r.Context(), minPrice)
	if err != nil {
		s.respondWithError(w, http.StatusInternalServerError, "failed to get post offices")
		return
	}

	var result []dto.PostOfficeByPriceResponse
	for _, po := range offices {
		if po == nil {
			continue
		}

		distributions, _ := s.distributionService.GetDistributionsByPostOfficeID(r.Context(), po.ID)

		newspapers := []dto.NewspaperByPriceDTO{}
		for _, d := range distributions {
			if d != nil && d.Newspaper != nil && d.Newspaper.PricePerCopy > minPrice {
				newspapers = append(newspapers, dto.NewspaperByPriceDTO{
					Title:    d.Newspaper.Title,
					Price:    d.Newspaper.PricePerCopy,
					Quantity: d.Quantity,
				})
			}
		}

		result = append(result, dto.PostOfficeByPriceResponse{
			PostOffice: dto.PostOfficeDTO{ID: po.ID, Number: po.Number, Address: po.Address},
			Newspapers: newspapers,
		})
	}

	s.respondWithJSON(w, http.StatusOK, result)
}

// handleGetPostOfficeFullDetail GET /post-offices/:id/full-detail
func (s *Server) handleGetPostOfficeFullDetail(w http.ResponseWriter, r *http.Request) {
	id, err := s.getIDFromURL(r)
	if err != nil {
		s.respondWithError(w, http.StatusBadRequest, "invalid post office ID")
		return
	}

	po, err := s.postOfficeService.GetPostOfficeByID(r.Context(), id)
	if err != nil {
		s.respondWithError(w, http.StatusNotFound, "post office not found")
		return
	}

	result := dto.PostOfficeDetailDTO{
		ID:            po.ID,
		Number:        po.Number,
		Address:       po.Address,
		Distributions: []dto.DistributionNestedDTO{},
	}

	s.respondWithJSON(w, http.StatusOK, result)
}
