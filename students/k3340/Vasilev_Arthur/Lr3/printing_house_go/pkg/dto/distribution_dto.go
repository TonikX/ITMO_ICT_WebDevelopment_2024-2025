package dto

// DistributionDTO represents distribution data transfer object
type DistributionDTO struct {
	ID                   int    `json:"id"`
	PostOfficeID         int    `json:"post_office_id"`
	PostOfficeNumber     string `json:"post_office_number,omitempty"`
	PostOfficeAddress    string `json:"post_office_address,omitempty"`
	NewspaperID          int    `json:"newspaper_id"`
	NewspaperTitle       string `json:"newspaper_title,omitempty"`
	NewspaperIndex       string `json:"newspaper_index,omitempty"`
	PrintingHouseID      int    `json:"printing_house_id"`
	PrintingHouseName    string `json:"printing_house_name,omitempty"`
	PrintingHouseAddress string `json:"printing_house_address,omitempty"`
	Quantity             int    `json:"quantity"`
}

// DistributionNestedDTO includes nested objects
type DistributionNestedDTO struct {
	ID            int              `json:"id"`
	Newspaper     NewspaperDTO     `json:"newspaper"`
	PrintingHouse PrintingHouseDTO `json:"printing_house"`
	Quantity      int              `json:"quantity"`
}

// CreateDistributionRequest for creating distribution
type CreateDistributionRequest struct {
	PostOfficeID    int `json:"post_office_id"`
	NewspaperID     int `json:"newspaper_id"`
	PrintingHouseID int `json:"printing_house_id"`
	Quantity        int `json:"quantity"`
}

// UpdateDistributionRequest for updating distribution
type UpdateDistributionRequest struct {
	Quantity *int `json:"quantity,omitempty"`
}
