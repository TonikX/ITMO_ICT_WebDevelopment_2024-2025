package main

import (
	"log"
	"net/http"
)

func main() {
	mux := setUpMux()

	err := run(mux)
	if err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}

func run(mux *http.ServeMux) error {
	err := http.ListenAndServe(":8080", mux)
	return err
}

func setUpMux() *http.ServeMux {
	mux := http.NewServeMux()
	return mux
}

func handleHomePage() {}

func handleNewGrade(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method is not allowed", http.StatusMethodNotAllowed)
	}
}
