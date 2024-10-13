package main

import (
	"log"
	"net/http"
)

func main() {
	fs := http.FileServer(http.Dir("./sakhnoya"))
	http.Handle("/", fs)

	log.Print("Listening on :3000...")
	err := http.ListenAndServe(":35213", nil)
	if err != nil {
		log.Fatal(err)
	}
}
