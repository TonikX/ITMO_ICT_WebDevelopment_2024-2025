package main

import (
	"fmt"
	"net"
)

const (
	clientMessage = "Hello, server"
)

func main() {
	conn, err := net.Dial("udp", "127.0.0.1:8080")
	if err != nil {
		fmt.Printf("failed to dial: %v", err)
	}
	defer conn.Close()

	_, err = conn.Write([]byte(clientMessage))
	if err != nil {
		fmt.Printf("failed to write: %v", err)
	}

	buffer := make([]byte, 1024)
	_, err = conn.Read(buffer)
	if err != nil {
		fmt.Printf("failed to read: %v", err)
	}

	fmt.Printf("message: %s", buffer)
}
