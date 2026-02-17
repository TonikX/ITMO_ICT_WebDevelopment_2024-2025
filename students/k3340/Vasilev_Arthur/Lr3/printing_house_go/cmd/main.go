package main

import (
	"log"

	"github.com/printing_house/internal/app"
)

func main() {
	if err := app.Run(); err != nil {
		log.Fatalf("Application error: %v", err)
	}
}
