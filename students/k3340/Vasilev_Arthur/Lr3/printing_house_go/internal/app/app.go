package app

import (
	"context"
	"log"
	"net/http"
	"time"

	"github.com/pkg/errors"
	"github.com/printing_house/deployment/config"
	"github.com/printing_house/internal/adapters/storage/postgres"
	"github.com/printing_house/internal/cases"
	port "github.com/printing_house/internal/ports/http"
)

// Run initializes and starts the application
func Run() error {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	cfg := config.NewConfig()

	log.Printf("Connecting to database: %s", cfg.PostgresDSN())

	repo, err := postgres.NewPgxClient(ctx, cfg.PostgresDSN())
	if err != nil {
		return errors.Wrap(err, "failed to create database client")
	}
	defer repo.Close()

	// Create services
	newspaperService, err := cases.NewNewspaperService(repo)
	if err != nil {
		return errors.Wrap(err, "failed to create newspaper service")
	}

	printingHouseService, err := cases.NewPrintingHouseService(repo)
	if err != nil {
		return errors.Wrap(err, "failed to create printing house service")
	}

	postOfficeService, err := cases.NewPostOfficeService(repo)
	if err != nil {
		return errors.Wrap(err, "failed to create post office service")
	}

	distributionService, err := cases.NewDistributionService(repo)
	if err != nil {
		return errors.Wrap(err, "failed to create distribution service")
	}

	printingRunService, err := cases.NewPrintingRunService(repo)
	if err != nil {
		return errors.Wrap(err, "failed to create printing run service")
	}

	tokenService, err := cases.NewTokenService(repo)
	if err != nil {
		return errors.Wrap(err, "failed to create token service")
	}

	userService, err := cases.NewUserService(repo)
	if err != nil {
		return errors.Wrap(err, "failed to create user service")
	}

	// Create HTTP server
	server, err := port.NewServer(
		newspaperService,
		printingHouseService,
		postOfficeService,
		distributionService,
		printingRunService,
		tokenService,
		userService,
		repo,
	)
	if err != nil {
		return errors.Wrap(err, "failed to create HTTP server")
	}

	// Start HTTP server
	httpServer := &http.Server{
		Addr:         cfg.HTTPAddr,
		Handler:      server,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	log.Printf("Starting HTTP server on %s", cfg.HTTPAddr)
	if err := httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		return errors.Wrap(err, "HTTP server error")
	}

	return nil
}
