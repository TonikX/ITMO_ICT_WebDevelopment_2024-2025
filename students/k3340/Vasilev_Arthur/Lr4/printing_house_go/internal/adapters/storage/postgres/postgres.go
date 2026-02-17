package postgres

import (
	"context"
	"github.com/jackc/pgx/v4/pgxpool"
	"github.com/pkg/errors"
	"github.com/printing_house/internal/entities"
)

// Client represents PostgreSQL database client
type Client struct {
	pool *pgxpool.Pool
}

// NewPgxClient creates a new PostgreSQL client
func NewPgxClient(ctx context.Context, dsn string) (*Client, error) {
	pool, err := pgxpool.Connect(ctx, dsn)
	if err != nil {
		return nil, errors.Wrap(err, "failed to connect to database")
	}

	if err := pool.Ping(ctx); err != nil {
		return nil, errors.Wrap(err, "failed to ping database")
	}

	return &Client{pool: pool}, nil
}

// Close closes the database connection
func (c *Client) Close() error {
	if c.pool != nil {
		c.pool.Close()
	}
	return nil
}

// ============ Newspaper Operations ============

// CreateNewspaper creates a new newspaper
func (c *Client) CreateNewspaper(ctx context.Context, n *entities.Newspaper) (*entities.Newspaper, error) {
	query := `
		INSERT INTO newspapers (title, publication_index, editor_first_name, editor_last_name, editor_middle_name, price_per_copy)
		VALUES ($1, $2, $3, $4, $5, $6)
		RETURNING id
	`

	row := c.pool.QueryRow(ctx, query,
		n.Title, n.PublicationIndex, n.EditorFirstName, n.EditorLastName, n.EditorMiddleName, n.PricePerCopy)

	if err := row.Scan(&n.ID); err != nil {
		return nil, errors.Wrap(err, "failed to create newspaper")
	}

	return n, nil
}

// GetNewspaperByID retrieves a newspaper by ID
func (c *Client) GetNewspaperByID(ctx context.Context, id int) (*entities.Newspaper, error) {
	query := `
		SELECT id, title, publication_index, editor_first_name, editor_last_name, editor_middle_name, price_per_copy
		FROM newspapers
		WHERE id = $1
	`

	n := &entities.Newspaper{}
	row := c.pool.QueryRow(ctx, query, id)

	if err := row.Scan(&n.ID, &n.Title, &n.PublicationIndex, &n.EditorFirstName, &n.EditorLastName, &n.EditorMiddleName, &n.PricePerCopy); err != nil {
		return nil, errors.Wrap(err, "failed to get newspaper")
	}

	return n, nil
}

// GetNewspaperByTitle retrieves a newspaper by title
func (c *Client) GetNewspaperByTitle(ctx context.Context, title string) (*entities.Newspaper, error) {
	query := `
		SELECT id, title, publication_index, editor_first_name, editor_last_name, editor_middle_name, price_per_copy
		FROM newspapers
		WHERE LOWER(title) = LOWER($1)
	`

	n := &entities.Newspaper{}
	row := c.pool.QueryRow(ctx, query, title)

	if err := row.Scan(&n.ID, &n.Title, &n.PublicationIndex, &n.EditorFirstName, &n.EditorLastName, &n.EditorMiddleName, &n.PricePerCopy); err != nil {
		return nil, errors.Wrap(err, "failed to get newspaper by title")
	}

	return n, nil
}

// GetAllNewspapers retrieves all newspapers
func (c *Client) GetAllNewspapers(ctx context.Context) ([]*entities.Newspaper, error) {
	query := `
		SELECT id, title, publication_index, editor_first_name, editor_last_name, editor_middle_name, price_per_copy
		FROM newspapers
		ORDER BY title
	`

	rows, err := c.pool.Query(ctx, query)
	if err != nil {
		return nil, errors.Wrap(err, "failed to get all newspapers")
	}
	defer rows.Close()

	var newspapers []*entities.Newspaper
	for rows.Next() {
		n := &entities.Newspaper{}
		if err := rows.Scan(&n.ID, &n.Title, &n.PublicationIndex, &n.EditorFirstName, &n.EditorLastName, &n.EditorMiddleName, &n.PricePerCopy); err != nil {
			return nil, errors.Wrap(err, "failed to scan newspaper")
		}
		newspapers = append(newspapers, n)
	}

	if err := rows.Err(); err != nil {
		return nil, errors.Wrap(err, "failed to read newspapers")
	}

	return newspapers, nil
}

// UpdateNewspaper updates a newspaper
func (c *Client) UpdateNewspaper(ctx context.Context, n *entities.Newspaper) (*entities.Newspaper, error) {
	query := `
		UPDATE newspapers
		SET title = $1, publication_index = $2, editor_first_name = $3, editor_last_name = $4, editor_middle_name = $5, price_per_copy = $6
		WHERE id = $7
		RETURNING id
	`

	err := c.pool.QueryRow(ctx, query,
		n.Title, n.PublicationIndex, n.EditorFirstName, n.EditorLastName, n.EditorMiddleName, n.PricePerCopy, n.ID).Scan(&n.ID)

	if err != nil {
		return nil, errors.Wrap(err, "failed to update newspaper")
	}

	return n, nil
}

// DeleteNewspaper deletes a newspaper
func (c *Client) DeleteNewspaper(ctx context.Context, id int) error {
	query := "DELETE FROM newspapers WHERE id = $1"
	_, err := c.pool.Exec(ctx, query, id)
	if err != nil {
		return errors.Wrap(err, "failed to delete newspaper")
	}
	return nil
}

// ============ PrintingHouse Operations ============

// CreatePrintingHouse creates a new printing house
func (c *Client) CreatePrintingHouse(ctx context.Context, ph *entities.PrintingHouse) (*entities.PrintingHouse, error) {
	query := `
		INSERT INTO printing_houses (name, address, is_active)
		VALUES ($1, $2, $3)
		RETURNING id
	`

	row := c.pool.QueryRow(ctx, query, ph.Name, ph.Address, ph.IsActive)

	if err := row.Scan(&ph.ID); err != nil {
		return nil, errors.Wrap(err, "failed to create printing house")
	}

	return ph, nil
}

// GetPrintingHouseByID retrieves a printing house by ID
func (c *Client) GetPrintingHouseByID(ctx context.Context, id int) (*entities.PrintingHouse, error) {
	query := `
		SELECT id, name, address, is_active
		FROM printing_houses
		WHERE id = $1
	`

	ph := &entities.PrintingHouse{}
	row := c.pool.QueryRow(ctx, query, id)

	if err := row.Scan(&ph.ID, &ph.Name, &ph.Address, &ph.IsActive); err != nil {
		return nil, errors.Wrap(err, "failed to get printing house")
	}

	return ph, nil
}

// GetAllPrintingHouses retrieves all active printing houses
func (c *Client) GetAllPrintingHouses(ctx context.Context) ([]*entities.PrintingHouse, error) {
	query := `
		SELECT id, name, address, is_active
		FROM printing_houses
		ORDER BY name
	`

	rows, err := c.pool.Query(ctx, query)
	if err != nil {
		return nil, errors.Wrap(err, "failed to get all printing houses")
	}
	defer rows.Close()

	var houses []*entities.PrintingHouse
	for rows.Next() {
		ph := &entities.PrintingHouse{}
		if err := rows.Scan(&ph.ID, &ph.Name, &ph.Address, &ph.IsActive); err != nil {
			return nil, errors.Wrap(err, "failed to scan printing house")
		}
		houses = append(houses, ph)
	}

	if err := rows.Err(); err != nil {
		return nil, errors.Wrap(err, "failed to read printing houses")
	}

	return houses, nil
}

// UpdatePrintingHouse updates a printing house
func (c *Client) UpdatePrintingHouse(ctx context.Context, ph *entities.PrintingHouse) (*entities.PrintingHouse, error) {
	query := `
		UPDATE printing_houses
		SET name = $1, address = $2, is_active = $3
		WHERE id = $4
		RETURNING id
	`

	err := c.pool.QueryRow(ctx, query, ph.Name, ph.Address, ph.IsActive, ph.ID).Scan(&ph.ID)

	if err != nil {
		return nil, errors.Wrap(err, "failed to update printing house")
	}

	return ph, nil
}

// DeletePrintingHouse deletes a printing house
func (c *Client) DeletePrintingHouse(ctx context.Context, id int) error {
	query := "DELETE FROM printing_houses WHERE id = $1"
	_, err := c.pool.Exec(ctx, query, id)
	if err != nil {
		return errors.Wrap(err, "failed to delete printing house")
	}
	return nil
}

// ============ PostOffice Operations ============

// CreatePostOffice creates a new post office
func (c *Client) CreatePostOffice(ctx context.Context, po *entities.PostOffice) (*entities.PostOffice, error) {
	query := `
		INSERT INTO post_offices (number, address)
		VALUES ($1, $2)
		RETURNING id
	`

	row := c.pool.QueryRow(ctx, query, po.Number, po.Address)

	if err := row.Scan(&po.ID); err != nil {
		return nil, errors.Wrap(err, "failed to create post office")
	}

	return po, nil
}

// GetPostOfficeByID retrieves a post office by ID
func (c *Client) GetPostOfficeByID(ctx context.Context, id int) (*entities.PostOffice, error) {
	query := `
		SELECT id, number, address
		FROM post_offices
		WHERE id = $1
	`

	po := &entities.PostOffice{}
	row := c.pool.QueryRow(ctx, query, id)

	if err := row.Scan(&po.ID, &po.Number, &po.Address); err != nil {
		return nil, errors.Wrap(err, "failed to get post office")
	}

	return po, nil
}

// GetAllPostOffices retrieves all post offices
func (c *Client) GetAllPostOffices(ctx context.Context) ([]*entities.PostOffice, error) {
	query := `
		SELECT id, number, address
		FROM post_offices
		ORDER BY number
	`

	rows, err := c.pool.Query(ctx, query)
	if err != nil {
		return nil, errors.Wrap(err, "failed to get all post offices")
	}
	defer rows.Close()

	var offices []*entities.PostOffice
	for rows.Next() {
		po := &entities.PostOffice{}
		if err := rows.Scan(&po.ID, &po.Number, &po.Address); err != nil {
			return nil, errors.Wrap(err, "failed to scan post office")
		}
		offices = append(offices, po)
	}

	if err := rows.Err(); err != nil {
		return nil, errors.Wrap(err, "failed to read post offices")
	}

	return offices, nil
}

// UpdatePostOffice updates a post office
func (c *Client) UpdatePostOffice(ctx context.Context, po *entities.PostOffice) (*entities.PostOffice, error) {
	query := `
		UPDATE post_offices
		SET number = $1, address = $2
		WHERE id = $3
		RETURNING id
	`

	err := c.pool.QueryRow(ctx, query, po.Number, po.Address, po.ID).Scan(&po.ID)

	if err != nil {
		return nil, errors.Wrap(err, "failed to update post office")
	}

	return po, nil
}

// DeletePostOffice deletes a post office
func (c *Client) DeletePostOffice(ctx context.Context, id int) error {
	query := "DELETE FROM post_offices WHERE id = $1"
	_, err := c.pool.Exec(ctx, query, id)
	if err != nil {
		return errors.Wrap(err, "failed to delete post office")
	}
	return nil
}

// ============ PrintingRun Operations ============

// CreatePrintingRun creates a new printing run
func (c *Client) CreatePrintingRun(ctx context.Context, pr *entities.PrintingRun) (*entities.PrintingRun, error) {
	query := `
		INSERT INTO printing_runs (printing_house_id, newspaper_id, circulation)
		VALUES ($1, $2, $3)
		RETURNING id
	`

	row := c.pool.QueryRow(ctx, query, pr.PrintingHouseID, pr.NewspaperID, pr.Circulation)

	if err := row.Scan(&pr.ID); err != nil {
		return nil, errors.Wrap(err, "failed to create printing run")
	}

	return pr, nil
}

// GetPrintingRunByID retrieves a printing run by ID
func (c *Client) GetPrintingRunByID(ctx context.Context, id int) (*entities.PrintingRun, error) {
	query := `
		SELECT id, printing_house_id, newspaper_id, circulation
		FROM printing_runs
		WHERE id = $1
	`

	pr := &entities.PrintingRun{}
	row := c.pool.QueryRow(ctx, query, id)

	if err := row.Scan(&pr.ID, &pr.PrintingHouseID, &pr.NewspaperID, &pr.Circulation); err != nil {
		return nil, errors.Wrap(err, "failed to get printing run")
	}

	return pr, nil
}

// GetPrintingRunsByNewspaperID retrieves all printing runs for a newspaper
func (c *Client) GetPrintingRunsByNewspaperID(ctx context.Context, newspaperID int) ([]*entities.PrintingRun, error) {
	query := `
		SELECT id, printing_house_id, newspaper_id, circulation
		FROM printing_runs
		WHERE newspaper_id = $1
		ORDER BY circulation DESC
	`

	rows, err := c.pool.Query(ctx, query, newspaperID)
	if err != nil {
		return nil, errors.Wrap(err, "failed to get printing runs")
	}
	defer rows.Close()

	var runs []*entities.PrintingRun
	for rows.Next() {
		pr := &entities.PrintingRun{}
		if err := rows.Scan(&pr.ID, &pr.PrintingHouseID, &pr.NewspaperID, &pr.Circulation); err != nil {
			return nil, errors.Wrap(err, "failed to scan printing run")
		}
		runs = append(runs, pr)
	}

	if err := rows.Err(); err != nil {
		return nil, errors.Wrap(err, "failed to read printing runs")
	}

	return runs, nil
}

// GetPrintingRunsByPrintingHouseID retrieves all printing runs for a printing house
func (c *Client) GetPrintingRunsByPrintingHouseID(ctx context.Context, printingHouseID int) ([]*entities.PrintingRun, error) {
	query := `
		SELECT id, printing_house_id, newspaper_id, circulation
		FROM printing_runs
		WHERE printing_house_id = $1
		ORDER BY circulation DESC
	`

	rows, err := c.pool.Query(ctx, query, printingHouseID)
	if err != nil {
		return nil, errors.Wrap(err, "failed to get printing runs")
	}
	defer rows.Close()

	var runs []*entities.PrintingRun
	for rows.Next() {
		pr := &entities.PrintingRun{}
		if err := rows.Scan(&pr.ID, &pr.PrintingHouseID, &pr.NewspaperID, &pr.Circulation); err != nil {
			return nil, errors.Wrap(err, "failed to scan printing run")
		}
		runs = append(runs, pr)
	}

	if err := rows.Err(); err != nil {
		return nil, errors.Wrap(err, "failed to read printing runs")
	}

	return runs, nil
}

// GetMaxCirculationForPrintingHouse retrieves the printing run with max circulation for a printing house
func (c *Client) GetMaxCirculationForPrintingHouse(ctx context.Context, printingHouseID int) (*entities.PrintingRun, error) {
	query := `
		SELECT pr.id, pr.printing_house_id, pr.newspaper_id, pr.circulation, 
		       n.id, n.title, n.publication_index, n.editor_first_name, n.editor_last_name, n.editor_middle_name, n.price_per_copy
		FROM printing_runs pr
		JOIN newspapers n ON pr.newspaper_id = n.id
		WHERE pr.printing_house_id = $1
		ORDER BY pr.circulation DESC
		LIMIT 1
	`

	pr := &entities.PrintingRun{}
	n := &entities.Newspaper{}

	row := c.pool.QueryRow(ctx, query, printingHouseID)

	if err := row.Scan(&pr.ID, &pr.PrintingHouseID, &pr.NewspaperID, &pr.Circulation,
		&n.ID, &n.Title, &n.PublicationIndex, &n.EditorFirstName, &n.EditorLastName, &n.EditorMiddleName, &n.PricePerCopy); err != nil {
		return nil, errors.Wrap(err, "failed to get max circulation printing run")
	}

	pr.Newspaper = n

	return pr, nil
}

// UpdatePrintingRun updates a printing run
func (c *Client) UpdatePrintingRun(ctx context.Context, pr *entities.PrintingRun) (*entities.PrintingRun, error) {
	query := `
		UPDATE printing_runs
		SET circulation = $1
		WHERE id = $2
		RETURNING id
	`

	err := c.pool.QueryRow(ctx, query, pr.Circulation, pr.ID).Scan(&pr.ID)

	if err != nil {
		return nil, errors.Wrap(err, "failed to update printing run")
	}

	return pr, nil
}

// DeletePrintingRun deletes a printing run
func (c *Client) DeletePrintingRun(ctx context.Context, id int) error {
	query := "DELETE FROM printing_runs WHERE id = $1"
	_, err := c.pool.Exec(ctx, query, id)
	if err != nil {
		return errors.Wrap(err, "failed to delete printing run")
	}
	return nil
}

// ============ Distribution Operations ============

// CreateDistribution creates a new distribution
func (c *Client) CreateDistribution(ctx context.Context, d *entities.Distribution) (*entities.Distribution, error) {
	query := `
		INSERT INTO distributions (post_office_id, newspaper_id, printing_house_id, quantity)
		VALUES ($1, $2, $3, $4)
		RETURNING id
	`

	row := c.pool.QueryRow(ctx, query, d.PostOfficeID, d.NewspaperID, d.PrintingHouseID, d.Quantity)

	if err := row.Scan(&d.ID); err != nil {
		return nil, errors.Wrap(err, "failed to create distribution")
	}

	return d, nil
}

// GetDistributionByID retrieves a distribution by ID
func (c *Client) GetDistributionByID(ctx context.Context, id int) (*entities.Distribution, error) {
	query := `
		SELECT id, post_office_id, newspaper_id, printing_house_id, quantity
		FROM distributions
		WHERE id = $1
	`

	d := &entities.Distribution{}
	row := c.pool.QueryRow(ctx, query, id)

	if err := row.Scan(&d.ID, &d.PostOfficeID, &d.NewspaperID, &d.PrintingHouseID, &d.Quantity); err != nil {
		return nil, errors.Wrap(err, "failed to get distribution")
	}

	return d, nil
}

// GetDistributionsByPostOfficeID retrieves distributions for a post office
func (c *Client) GetDistributionsByPostOfficeID(ctx context.Context, postOfficeID int) ([]*entities.Distribution, error) {
	query := `
		SELECT d.id, d.post_office_id, d.newspaper_id, d.printing_house_id, d.quantity,
		       po.number, po.address,
		       n.title, n.publication_index, n.price_per_copy,
		       ph.name, ph.address
		FROM distributions d
		JOIN post_offices po ON d.post_office_id = po.id
		JOIN newspapers n ON d.newspaper_id = n.id
		JOIN printing_houses ph ON d.printing_house_id = ph.id
		WHERE d.post_office_id = $1
		ORDER BY n.title
	`

	rows, err := c.pool.Query(ctx, query, postOfficeID)
	if err != nil {
		return nil, errors.Wrap(err, "failed to get distributions")
	}
	defer rows.Close()

	var distributions []*entities.Distribution
	for rows.Next() {
		d := &entities.Distribution{}
		po := &entities.PostOffice{}
		n := &entities.Newspaper{}
		ph := &entities.PrintingHouse{}

		if err := rows.Scan(&d.ID, &d.PostOfficeID, &d.NewspaperID, &d.PrintingHouseID, &d.Quantity,
			&po.ID, &po.Number, &po.Address,
			&n.ID, &n.Title, &n.PublicationIndex, &n.PricePerCopy,
			&ph.ID, &ph.Name, &ph.Address); err != nil {
			return nil, errors.Wrap(err, "failed to scan distribution")
		}

		po.ID = postOfficeID
		d.PostOffice = po
		d.Newspaper = n
		d.PrintingHouse = ph

		distributions = append(distributions, d)
	}

	if err := rows.Err(); err != nil {
		return nil, errors.Wrap(err, "failed to read distributions")
	}

	return distributions, nil
}

// GetDistributionsByNewspaperID retrieves distributions for a newspaper
func (c *Client) GetDistributionsByNewspaperID(ctx context.Context, newspaperID int) ([]*entities.Distribution, error) {
	query := `
		SELECT d.id, d.post_office_id, d.newspaper_id, d.printing_house_id, d.quantity
		FROM distributions d
		WHERE d.newspaper_id = $1
		ORDER BY d.id
	`

	rows, err := c.pool.Query(ctx, query, newspaperID)
	if err != nil {
		return nil, errors.Wrap(err, "failed to get distributions")
	}
	defer rows.Close()

	var distributions []*entities.Distribution
	for rows.Next() {
		d := &entities.Distribution{}
		if err := rows.Scan(&d.ID, &d.PostOfficeID, &d.NewspaperID, &d.PrintingHouseID, &d.Quantity); err != nil {
			return nil, errors.Wrap(err, "failed to scan distribution")
		}
		distributions = append(distributions, d)
	}

	if err := rows.Err(); err != nil {
		return nil, errors.Wrap(err, "failed to read distributions")
	}

	return distributions, nil
}

// GetDistributionsByPrintingHouseID retrieves distributions for a printing house
func (c *Client) GetDistributionsByPrintingHouseID(ctx context.Context, printingHouseID int) ([]*entities.Distribution, error) {
	query := `
		SELECT d.id, d.post_office_id, d.newspaper_id, d.printing_house_id, d.quantity
		FROM distributions d
		WHERE d.printing_house_id = $1
		ORDER BY d.id
	`

	rows, err := c.pool.Query(ctx, query, printingHouseID)
	if err != nil {
		return nil, errors.Wrap(err, "failed to get distributions")
	}
	defer rows.Close()

	var distributions []*entities.Distribution
	for rows.Next() {
		d := &entities.Distribution{}
		if err := rows.Scan(&d.ID, &d.PostOfficeID, &d.NewspaperID, &d.PrintingHouseID, &d.Quantity); err != nil {
			return nil, errors.Wrap(err, "failed to scan distribution")
		}
		distributions = append(distributions, d)
	}

	if err := rows.Err(); err != nil {
		return nil, errors.Wrap(err, "failed to read distributions")
	}

	return distributions, nil
}

// GetPostOfficesByNewspaperPrice retrieves post offices that receive newspapers with price > minPrice
func (c *Client) GetPostOfficesByNewspaperPrice(ctx context.Context, minPrice float64) ([]*entities.PostOffice, error) {
	query := `
		SELECT DISTINCT po.id, po.number, po.address
		FROM post_offices po
		JOIN distributions d ON po.id = d.post_office_id
		JOIN newspapers n ON d.newspaper_id = n.id
		WHERE n.price_per_copy > $1
		ORDER BY po.number
	`

	rows, err := c.pool.Query(ctx, query, minPrice)
	if err != nil {
		return nil, errors.Wrap(err, "failed to get post offices by price")
	}
	defer rows.Close()

	var offices []*entities.PostOffice
	for rows.Next() {
		po := &entities.PostOffice{}
		if err := rows.Scan(&po.ID, &po.Number, &po.Address); err != nil {
			return nil, errors.Wrap(err, "failed to scan post office")
		}
		offices = append(offices, po)
	}

	if err := rows.Err(); err != nil {
		return nil, errors.Wrap(err, "failed to read post offices")
	}

	if len(offices) == 0 {
		return offices, nil
	}

	return offices, nil
}

// UpdateDistribution updates a distribution
func (c *Client) UpdateDistribution(ctx context.Context, d *entities.Distribution) (*entities.Distribution, error) {
	query := `
		UPDATE distributions
		SET quantity = $1
		WHERE id = $2
		RETURNING id
	`

	err := c.pool.QueryRow(ctx, query, d.Quantity, d.ID).Scan(&d.ID)

	if err != nil {
		return nil, errors.Wrap(err, "failed to update distribution")
	}

	return d, nil
}

// DeleteDistribution deletes a distribution
func (c *Client) DeleteDistribution(ctx context.Context, id int) error {
	query := "DELETE FROM distributions WHERE id = $1"
	_, err := c.pool.Exec(ctx, query, id)
	if err != nil {
		return errors.Wrap(err, "failed to delete distribution")
	}
	return nil
}
// ============ APIToken Operations ============

// GetAPITokenByToken retrieves token by token string
func (c *Client) GetAPITokenByToken(ctx context.Context, token string) (*entities.APIToken, error) {
	query := `
		SELECT id, token, name, expires_at, created_at, is_active
		FROM api_tokens
		WHERE token = $1
	`
	row := c.pool.QueryRow(ctx, query, token)

	var t entities.APIToken
	if err := row.Scan(&t.ID, &t.Token, &t.Name, &t.ExpiresAt, &t.CreatedAt, &t.IsActive); err != nil {
		return nil, errors.Wrap(err, "failed to get API token")
	}

	return &t, nil
}

// CreateAPIToken creates a new API token
func (c *Client) CreateAPIToken(ctx context.Context, token *entities.APIToken) (*entities.APIToken, error) {
	query := `
		INSERT INTO api_tokens (token, name, expires_at, is_active)
		VALUES ($1, $2, $3, $4)
		RETURNING id, created_at
	`
	row := c.pool.QueryRow(ctx, query, token.Token, token.Name, token.ExpiresAt, token.IsActive)

	if err := row.Scan(&token.ID, &token.CreatedAt); err != nil {
		return nil, errors.Wrap(err, "failed to create API token")
	}

	return token, nil
}

// GetAllAPITokens retrieves all API tokens
func (c *Client) GetAllAPITokens(ctx context.Context) ([]*entities.APIToken, error) {
	query := `
		SELECT id, token, name, expires_at, created_at, is_active
		FROM api_tokens
		ORDER BY created_at DESC
	`
	rows, err := c.pool.Query(ctx, query)
	if err != nil {
		return nil, errors.Wrap(err, "failed to get API tokens")
	}
	defer rows.Close()

	var tokens []*entities.APIToken
	for rows.Next() {
		var t entities.APIToken
		if err := rows.Scan(&t.ID, &t.Token, &t.Name, &t.ExpiresAt, &t.CreatedAt, &t.IsActive); err != nil {
			return nil, errors.Wrap(err, "failed to scan API token")
		}
		tokens = append(tokens, &t)
	}

	return tokens, nil
}

// RevokeAPIToken revokes an API token by marking it inactive
func (c *Client) RevokeAPIToken(ctx context.Context, token string) error {
	query := "UPDATE api_tokens SET is_active = FALSE WHERE token = $1"
	_, err := c.pool.Exec(ctx, query, token)
	if err != nil {
		return errors.Wrap(err, "failed to revoke API token")
	}
	return nil
}

// ============ User Operations ============

// CreateUser creates a new user
func (c *Client) CreateUser(ctx context.Context, user *entities.User) (*entities.User, error) {
	query := `
		INSERT INTO users (username, email, password_hash, first_name, last_name, is_active)
		VALUES ($1, $2, $3, $4, $5, $6)
		RETURNING id, created_at, updated_at
	`

	row := c.pool.QueryRow(ctx, query,
		user.Username, user.Email, user.PasswordHash, user.FirstName, user.LastName, user.IsActive)

	if err := row.Scan(&user.ID, &user.CreatedAt, &user.UpdatedAt); err != nil {
		return nil, errors.Wrap(err, "failed to create user")
	}

	return user, nil
}

// GetUserByID retrieves a user by ID
func (c *Client) GetUserByID(ctx context.Context, id int) (*entities.User, error) {
	query := `
		SELECT id, username, email, password_hash, first_name, last_name, is_active, created_at, updated_at
		FROM users
		WHERE id = $1
	`

	user := &entities.User{}
	row := c.pool.QueryRow(ctx, query, id)

	if err := row.Scan(&user.ID, &user.Username, &user.Email, &user.PasswordHash, 
		&user.FirstName, &user.LastName, &user.IsActive, &user.CreatedAt, &user.UpdatedAt); err != nil {
		return nil, errors.Wrap(err, "failed to get user by ID")
	}

	return user, nil
}

// GetUserByUsername retrieves a user by username
func (c *Client) GetUserByUsername(ctx context.Context, username string) (*entities.User, error) {
	query := `
		SELECT id, username, email, password_hash, first_name, last_name, is_active, created_at, updated_at
		FROM users
		WHERE username = $1
	`

	user := &entities.User{}
	row := c.pool.QueryRow(ctx, query, username)

	if err := row.Scan(&user.ID, &user.Username, &user.Email, &user.PasswordHash,
		&user.FirstName, &user.LastName, &user.IsActive, &user.CreatedAt, &user.UpdatedAt); err != nil {
		return nil, errors.Wrap(err, "failed to get user by username")
	}

	return user, nil
}

// GetUserByEmail retrieves a user by email
func (c *Client) GetUserByEmail(ctx context.Context, email string) (*entities.User, error) {
	query := `
		SELECT id, username, email, password_hash, first_name, last_name, is_active, created_at, updated_at
		FROM users
		WHERE email = $1
	`

	user := &entities.User{}
	row := c.pool.QueryRow(ctx, query, email)

	if err := row.Scan(&user.ID, &user.Username, &user.Email, &user.PasswordHash,
		&user.FirstName, &user.LastName, &user.IsActive, &user.CreatedAt, &user.UpdatedAt); err != nil {
		return nil, errors.Wrap(err, "failed to get user by email")
	}

	return user, nil
}

// GetAllUsers retrieves all users
func (c *Client) GetAllUsers(ctx context.Context) ([]*entities.User, error) {
	query := `
		SELECT id, username, email, password_hash, first_name, last_name, is_active, created_at, updated_at
		FROM users
		ORDER BY created_at DESC
	`

	rows, err := c.pool.Query(ctx, query)
	if err != nil {
		return nil, errors.Wrap(err, "failed to get all users")
	}
	defer rows.Close()

	var users []*entities.User
	for rows.Next() {
		user := &entities.User{}
		if err := rows.Scan(&user.ID, &user.Username, &user.Email, &user.PasswordHash,
			&user.FirstName, &user.LastName, &user.IsActive, &user.CreatedAt, &user.UpdatedAt); err != nil {
			return nil, errors.Wrap(err, "failed to scan user")
		}
		users = append(users, user)
	}

	return users, nil
}

// UpdateUser updates a user
func (c *Client) UpdateUser(ctx context.Context, user *entities.User) (*entities.User, error) {
	query := `
		UPDATE users
		SET username = $1, email = $2, first_name = $3, last_name = $4, is_active = $5, updated_at = NOW()
		WHERE id = $6
		RETURNING updated_at
	`

	err := c.pool.QueryRow(ctx, query,
		user.Username, user.Email, user.FirstName, user.LastName, user.IsActive, user.ID).Scan(&user.UpdatedAt)

	if err != nil {
		return nil, errors.Wrap(err, "failed to update user")
	}

	return user, nil
}

// DeleteUser deletes a user
func (c *Client) DeleteUser(ctx context.Context, id int) error {
	query := "DELETE FROM users WHERE id = $1"
	_, err := c.pool.Exec(ctx, query, id)
	if err != nil {
		return errors.Wrap(err, "failed to delete user")
	}
	return nil
}