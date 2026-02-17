package dto

// PrintingRunNestedDTO includes nested objects
type PrintingRunNestedDTO struct {
	ID          int          `json:"id"`
	Newspaper   NewspaperDTO `json:"newspaper"`
	Circulation int          `json:"circulation"`
}
