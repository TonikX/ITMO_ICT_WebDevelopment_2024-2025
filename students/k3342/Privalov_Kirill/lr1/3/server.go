package main

import (
	"html/template"
	"log"
	"net/http"
	"os"
	"path/filepath"
)

var tmpl *template.Template

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", handleHomePage)

	err := http.ListenAndServe(":8080", mux)
	if err != nil {
		log.Fatalf("Failed to start server")
	}
}

func init() {
	cwd, err := os.Getwd()
	if err != nil {
		log.Fatalf("Failed to get current working directory: %v", err)
	}

	tmplPath := filepath.Join(cwd, "students", "k3342", "Privalov_Kirill", "lr1", "3", "static", "index.html")
	tmpl, err = template.ParseFiles(tmplPath)
	if err != nil {
		log.Fatalf("[server][ParseFiles]: %v", err)
	}
}

func handleHomePage(w http.ResponseWriter, r *http.Request) {
	err := tmpl.Execute(w, nil)
	if err != nil {
		log.Fatalf("Failed to parse index.html")
	}
}
