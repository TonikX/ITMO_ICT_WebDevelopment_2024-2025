package main

import (
	"context"
	"flag"
	"fmt"
	utils "lab_1"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	// settings
	logger := utils.NewLogger("server")
	port := flag.String("p", "", "Port of the server")
	flag.Parse()

	if port == nil || *port == "" {
		logger.LogFatal("must specify a port to connect to")
	}

	// create http server
	srv := &http.Server{Addr: *port}

	// handling all endpoints with "/"
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html")
		http.ServeFile(w, r, "index.html")
	})

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)

	// starting server
	go func() {
		logMsg := fmt.Sprintf("Your endpoint is: http://localhost%s", *port)
		logger.LogMessage(http.StatusOK, logMsg)

		if err := srv.ListenAndServe(); err != nil && err.Error() != http.ErrServerClosed.Error() {
			errMsg := fmt.Sprintf("server failed to start: %v", err)
			logger.LogMessage(http.StatusInternalServerError, errMsg)
		}
	}()

	// shutdown server with ^C
	<-quit
	logger.LogMessage(http.StatusOK, "shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		errMsg := fmt.Sprintf("server shutdown failed: %v", err)
		logger.LogMessage(http.StatusInternalServerError, errMsg)
	}

	logger.LogMessage(http.StatusOK, "server stopped")
}
