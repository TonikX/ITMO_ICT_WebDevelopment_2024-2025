package dto

// ErrorResponse represents error response
type ErrorResponse struct {
	Error string `json:"error"`
}

// ByNameResponse for Newspaper by_name action
type ByNameResponse struct {
	Newspaper         NewspaperDTO         `json:"newspaper"`
	PrintingAddresses []PrintingAddressDTO `json:"printing_addresses"`
}

// PrintingAddressDTO for printing address info
type PrintingAddressDTO struct {
	PrintingHouse string `json:"printing_house"`
	Address       string `json:"address"`
	Circulation   int    `json:"circulation"`
}
