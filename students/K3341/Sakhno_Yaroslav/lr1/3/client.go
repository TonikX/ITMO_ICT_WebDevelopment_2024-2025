package main

import (
	"fmt"
	"io"
	"net/http"
)

func main() {
	resp, err := http.Get("http://localhost:3000/index.html")
	if err != nil {
		fmt.Println(err)
		// handle error
		return
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)

	print(string(body))
}
