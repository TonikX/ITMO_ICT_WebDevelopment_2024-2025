package main

import (
	"fmt"
	"net/http"
)

func main() {
	fs := http.FileServer(http.Dir("."))
	err := http.ListenAndServe("localhost:8080", fs)
	if err != nil {
		fmt.Sprintf("failed to listen: %v", err)
		return
	}
}
