package cases

import (
	"context"

	"github.com/printing_house/internal/entities"
)

// Repository interface defines all database operations
type Repository interface {
	// Newspaper operations
	CreateNewspaper(ctx context.Context, n *entities.Newspaper) (*entities.Newspaper, error)
	GetNewspaperByID(ctx context.Context, id int) (*entities.Newspaper, error)
	GetNewspaperByTitle(ctx context.Context, title string) (*entities.Newspaper, error)
	GetAllNewspapers(ctx context.Context) ([]*entities.Newspaper, error)
	UpdateNewspaper(ctx context.Context, n *entities.Newspaper) (*entities.Newspaper, error)
	DeleteNewspaper(ctx context.Context, id int) error

	// PrintingHouse operations
	CreatePrintingHouse(ctx context.Context, ph *entities.PrintingHouse) (*entities.PrintingHouse, error)
	GetPrintingHouseByID(ctx context.Context, id int) (*entities.PrintingHouse, error)
	GetAllPrintingHouses(ctx context.Context) ([]*entities.PrintingHouse, error)
	UpdatePrintingHouse(ctx context.Context, ph *entities.PrintingHouse) (*entities.PrintingHouse, error)
	DeletePrintingHouse(ctx context.Context, id int) error

	// PostOffice operations
	CreatePostOffice(ctx context.Context, po *entities.PostOffice) (*entities.PostOffice, error)
	GetPostOfficeByID(ctx context.Context, id int) (*entities.PostOffice, error)
	GetAllPostOffices(ctx context.Context) ([]*entities.PostOffice, error)
	UpdatePostOffice(ctx context.Context, po *entities.PostOffice) (*entities.PostOffice, error)
	DeletePostOffice(ctx context.Context, id int) error

	// PrintingRun operations
	CreatePrintingRun(ctx context.Context, pr *entities.PrintingRun) (*entities.PrintingRun, error)
	GetPrintingRunByID(ctx context.Context, id int) (*entities.PrintingRun, error)
	GetAllPrintingRuns(ctx context.Context) ([]*entities.PrintingRun, error)
	GetPrintingRunsByNewspaperID(ctx context.Context, newspaperID int) ([]*entities.PrintingRun, error)
	GetPrintingRunsByPrintingHouseID(ctx context.Context, printingHouseID int) ([]*entities.PrintingRun, error)
	GetMaxCirculationForPrintingHouse(ctx context.Context, printingHouseID int) (*entities.PrintingRun, error)
	UpdatePrintingRun(ctx context.Context, pr *entities.PrintingRun) (*entities.PrintingRun, error)
	DeletePrintingRun(ctx context.Context, id int) error

	// Distribution operations
	CreateDistribution(ctx context.Context, d *entities.Distribution) (*entities.Distribution, error)
	GetDistributionByID(ctx context.Context, id int) (*entities.Distribution, error)
	GetAllDistributions(ctx context.Context) ([]*entities.Distribution, error)
	GetDistributionsByPostOfficeID(ctx context.Context, postOfficeID int) ([]*entities.Distribution, error)
	GetDistributionsByNewspaperID(ctx context.Context, newspaperID int) ([]*entities.Distribution, error)
	GetDistributionsByPrintingHouseID(ctx context.Context, printingHouseID int) ([]*entities.Distribution, error)
	GetPostOfficesByNewspaperPrice(ctx context.Context, minPrice float64) ([]*entities.PostOffice, error)
	UpdateDistribution(ctx context.Context, d *entities.Distribution) (*entities.Distribution, error)
	DeleteDistribution(ctx context.Context, id int) error

	// APIToken operations
	GetAPITokenByToken(ctx context.Context, token string) (*entities.APIToken, error)
	CreateAPIToken(ctx context.Context, token *entities.APIToken) (*entities.APIToken, error)
	GetAllAPITokens(ctx context.Context) ([]*entities.APIToken, error)
	RevokeAPIToken(ctx context.Context, token string) error

	// User operations
	CreateUser(ctx context.Context, user *entities.User) (*entities.User, error)
	GetUserByID(ctx context.Context, id int) (*entities.User, error)
	GetUserByUsername(ctx context.Context, username string) (*entities.User, error)
	GetUserByEmail(ctx context.Context, email string) (*entities.User, error)
	GetAllUsers(ctx context.Context) ([]*entities.User, error)
	UpdateUser(ctx context.Context, user *entities.User) (*entities.User, error)
	DeleteUser(ctx context.Context, id int) error

	Close() error
}
