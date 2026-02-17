package dto

// PrintingHouseDTO represents printing house data transfer object
type PrintingHouseDTO struct {
	ID       int    `json:"id"`
	Name     string `json:"name"`
	Address  string `json:"address"`
	IsActive bool   `json:"is_active"`
}

// PrintingHouseDetailDTO includes nested relationships
type PrintingHouseDetailDTO struct {
	ID           int                    `json:"id"`
	Name         string                 `json:"name"`
	Address      string                 `json:"address"`
	IsActive     bool                   `json:"is_active"`
	PrintingRuns []PrintingRunNestedDTO `json:"printing_runs"`
}

// CreatePrintingHouseRequest for creating printing house
type CreatePrintingHouseRequest struct {
	Name     string `json:"name"`
	Address  string `json:"address"`
	IsActive bool   `json:"is_active"`
}

// UpdatePrintingHouseRequest for updating printing house
type UpdatePrintingHouseRequest struct {
	Name     *string `json:"name,omitempty"`
	Address  *string `json:"address,omitempty"`
	IsActive *bool   `json:"is_active,omitempty"`
}

// LargestCirculationEditorResponse for largest circulation editor response
type LargestCirculationEditorResponse struct {
	PrintingHouse  string `json:"printing_house"`
	Newspaper      string `json:"newspaper"`
	Circulation    int    `json:"circulation"`
	EditorLastName string `json:"editor_last_name"`
	EditorFullName string `json:"editor_full_name"`
}

// PrintingHouseReportResponse for report action
type PrintingHouseReportResponse struct {
	PrintingHouse   PrintingHouseDTO         `json:"printing_house"`
	TotalNewspapers int                      `json:"total_newspapers"`
	Newspapers      []NewspaperReportItemDTO `json:"newspapers"`
}

// NewspaperReportItemDTO for report newspaper item
type NewspaperReportItemDTO struct {
	Newspaper        string                      `json:"newspaper"`
	Circulation      int                         `json:"circulation"`
	Distributions    []DistributionReportItemDTO `json:"distributions"`
	TotalDistributed int                         `json:"total_distributed"`
}

// DistributionReportItemDTO for report distribution item
type DistributionReportItemDTO struct {
	PostOfficeNumber  string `json:"post_office_number"`
	PostOfficeAddress string `json:"post_office_address"`
	Quantity          int    `json:"quantity"`
}
