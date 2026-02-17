package dto

// PrintingRunDTO represents printing run data transfer object
type PrintingRunDTO struct {
	ID              int    `json:"id"`
	PrintingHouseID int    `json:"printing_house_id"`
	NewspaperID     int    `json:"newspaper_id"`
	Circulation     int    `json:"circulation"`
	PrintingHouseName    string `json:"printing_house_name,omitempty"`
	PrintingHouseAddress string `json:"printing_house_address,omitempty"`
	NewspaperTitle       string `json:"newspaper_title,omitempty"`
	NewspaperIndex       string `json:"newspaper_index,omitempty"`
}

// PrintingRunNestedDTO includes nested objects
type PrintingRunNestedDTO struct {
	ID            int              `json:"id"`
	Newspaper     NewspaperDTO     `json:"newspaper"`
	PrintingHouse PrintingHouseDTO `json:"printing_house"`
	Circulation   int              `json:"circulation"`
}

// CreatePrintingRunRequest for creating printing run
type CreatePrintingRunRequest struct {
	PrintingHouseID int `json:"printing_house_id"`
	NewspaperID     int `json:"newspaper_id"`
	Circulation     int `json:"circulation"`
}

// UpdatePrintingRunRequest for updating printing run
type UpdatePrintingRunRequest struct {
	Circulation *int `json:"circulation,omitempty"`
}
