package config

import (
	"log"
	"time"

	"github.com/spf13/viper"
)

// Config represents application configuration
type Config struct {
	HTTPAddr      string
	FetchInterval time.Duration
	HTTPPort      string
}

// NewConfig creates a new configuration from environment or config file
func NewConfig() *Config {
	viper.SetConfigName("config")
	viper.SetConfigType("yml")
	viper.AddConfigPath(".")
	viper.AddConfigPath("./deployment/config")
	viper.AddConfigPath("../deployment/config")
	viper.AddConfigPath("../../deployment/config")

	// Set defaults
	viper.SetDefault("postgres_dsn", "postgres://user:password@localhost:5432/printing_house?sslmode=disable")
	viper.SetDefault("http_addr", ":8080")
	viper.SetDefault("fetch_interval", "10s")

	// Try to read config file, but don't fail if it doesn't exist
	if err := viper.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); !ok {
			log.Printf("Error reading config file: %v", err)
		}
		log.Println("Using default configuration")
	}

	// Read from environment variables
	viper.SetEnvPrefix("PRINTING_HOUSE")
	viper.AutomaticEnv()

	httpAddrStr := viper.GetString("http_addr")
	intervalStr := viper.GetString("fetch_interval")

	interval, err := time.ParseDuration(intervalStr)
	if err != nil {
		interval = 10 * time.Second
	}

	return &Config{
		HTTPAddr:      httpAddrStr,
		FetchInterval: interval,
	}
}

func (c *Config) PostgresDSN() string {
	connString := viper.GetString("postgres_dsn")
	return connString
}
