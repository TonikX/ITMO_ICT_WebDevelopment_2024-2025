-- Database migrations for printing_house
BEGIN;

-- Create newspapers table
CREATE TABLE IF NOT EXISTS newspapers (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    publication_index VARCHAR(20) NOT NULL UNIQUE,
    editor_first_name VARCHAR(100) NOT NULL,
    editor_last_name VARCHAR(100) NOT NULL,
    editor_middle_name VARCHAR(100),
    price_per_copy DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create printing_houses table
CREATE TABLE IF NOT EXISTS printing_houses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    address TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create post_offices table
CREATE TABLE IF NOT EXISTS post_offices (
    id SERIAL PRIMARY KEY,
    number VARCHAR(20) NOT NULL UNIQUE,
    address TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create printing_runs table (многие-ко-многим между newspapers и printing_houses)
CREATE TABLE IF NOT EXISTS printing_runs (
    id SERIAL PRIMARY KEY,
    printing_house_id INTEGER NOT NULL REFERENCES printing_houses(id) ON DELETE CASCADE,
    newspaper_id INTEGER NOT NULL REFERENCES newspapers(id) ON DELETE CASCADE,
    circulation INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(printing_house_id, newspaper_id)
);

-- Create distributions table (многие-ко-многим между post_offices, newspapers и printing_houses)
CREATE TABLE IF NOT EXISTS distributions (
    id SERIAL PRIMARY KEY,
    post_office_id INTEGER NOT NULL REFERENCES post_offices(id) ON DELETE CASCADE,
    newspaper_id INTEGER NOT NULL REFERENCES newspapers(id) ON DELETE CASCADE,
    printing_house_id INTEGER NOT NULL REFERENCES printing_houses(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(post_office_id, newspaper_id, printing_house_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_newspapers_title ON newspapers(title);
CREATE INDEX idx_newspapers_publication_index ON newspapers(publication_index);
CREATE INDEX idx_printing_houses_name ON printing_houses(name);
CREATE INDEX idx_post_offices_number ON post_offices(number);
CREATE INDEX idx_printing_runs_printing_house ON printing_runs(printing_house_id);
CREATE INDEX idx_printing_runs_newspaper ON printing_runs(newspaper_id);
CREATE INDEX idx_distributions_post_office ON distributions(post_office_id);
CREATE INDEX idx_distributions_newspaper ON distributions(newspaper_id);
CREATE INDEX idx_distributions_printing_house ON distributions(printing_house_id);

COMMIT;
