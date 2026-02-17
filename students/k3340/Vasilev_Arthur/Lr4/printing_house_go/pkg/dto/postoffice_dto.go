package dto

// PostOfficeDTO represents post office data transfer object
type PostOfficeDTO struct {
	ID      int    `json:"id"`
	Number  string `json:"number"`
	Address string `json:"address"`
}

// PostOfficeDetailDTO includes nested relationships
type PostOfficeDetailDTO struct {
	ID            int                     `json:"id"`
	Number        string                  `json:"number"`
	Address       string                  `json:"address"`
	Distributions []DistributionNestedDTO `json:"distributions"`
}

// CreatePostOfficeRequest for creating post office
type CreatePostOfficeRequest struct {
	Number  string `json:"number"`
	Address string `json:"address"`
}

// UpdatePostOfficeRequest for updating post office
type UpdatePostOfficeRequest struct {
	Number  *string `json:"number,omitempty"`
	Address *string `json:"address,omitempty"`
}

// PostOfficeByPriceResponse for by_price action response
type PostOfficeByPriceResponse struct {
	PostOffice PostOfficeDTO         `json:"post_office"`
	Newspapers []NewspaperByPriceDTO `json:"newspapers"`
}

// NewspaperByPriceDTO for newspaper in by_price response
type NewspaperByPriceDTO struct {
	Title    string  `json:"title"`
	Price    float64 `json:"price"`
	Quantity int     `json:"quantity"`
}
