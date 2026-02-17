package dto

// NewspaperDTO represents newspaper data transfer object
type NewspaperDTO struct {
	ID               int     `json:"id"`
	Title            string  `json:"title"`
	PublicationIndex string  `json:"publication_index"`
	EditorFirstName  string  `json:"editor_first_name"`
	EditorLastName   string  `json:"editor_last_name"`
	EditorMiddleName *string `json:"editor_middle_name,omitempty"`
	EditorFullName   string  `json:"editor_full_name"`
	PricePerCopy     float64 `json:"price_per_copy"`
}

// NewspaperDetailDTO includes nested relationships
type NewspaperDetailDTO struct {
	ID               int                     `json:"id"`
	Title            string                  `json:"title"`
	PublicationIndex string                  `json:"publication_index"`
	EditorFirstName  string                  `json:"editor_first_name"`
	EditorLastName   string                  `json:"editor_last_name"`
	EditorMiddleName *string                 `json:"editor_middle_name,omitempty"`
	EditorFullName   string                  `json:"editor_full_name"`
	PricePerCopy     float64                 `json:"price_per_copy"`
	PrintingRuns     []PrintingRunNestedDTO  `json:"printing_runs"`
	Distributions    []DistributionNestedDTO `json:"distributions"`
}

// NewspaperInfoDTO for info action response
type NewspaperInfoDTO struct {
	Title            string  `json:"title"`
	PublicationIndex string  `json:"publication_index"`
	PricePerCopy     float64 `json:"price_per_copy"`
	Editor           string  `json:"editor"`
}

// CreateNewspaperRequest for creating newspaper
type CreateNewspaperRequest struct {
	Title            string  `json:"title"`
	PublicationIndex string  `json:"publication_index"`
	EditorFirstName  string  `json:"editor_first_name"`
	EditorLastName   string  `json:"editor_last_name"`
	EditorMiddleName *string `json:"editor_middle_name"`
	PricePerCopy     float64 `json:"price_per_copy"`
}

// UpdateNewspaperRequest for updating newspaper
type UpdateNewspaperRequest struct {
	Title            *string  `json:"title,omitempty"`
	PublicationIndex *string  `json:"publication_index,omitempty"`
	EditorFirstName  *string  `json:"editor_first_name,omitempty"`
	EditorLastName   *string  `json:"editor_last_name,omitempty"`
	EditorMiddleName *string  `json:"editor_middle_name,omitempty"`
	PricePerCopy     *float64 `json:"price_per_copy,omitempty"`
}
