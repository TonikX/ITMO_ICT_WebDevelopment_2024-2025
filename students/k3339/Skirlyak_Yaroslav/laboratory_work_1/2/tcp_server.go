package main

import (
	"fmt"
	"net"
)

const (
	serverMessage = "Hello, client"
	port          = 8080
	host          = "127.0.0.1"
)

func main() {
	server, err := net.Listen("tcp", fmt.Sprintf("%s:%d", host, port))
	if err != nil {
		fmt.Printf("failed to listen: %v", err)
	}
	defer server.Close()

	fmt.Printf("server started on %s:%d\n", host, port)

	for {
		conn, err := server.Accept()
		if err != nil {
			fmt.Printf("failed to accept: %v", err)
		}

		fmt.Println("client connected")

		go handleClient(conn)
	}
}

func handleClient(conn net.Conn) {
	fmt.Println("handling client")

	buffer := make([]byte, 1024)

	fmt.Println("reading message from client")

	_, err := conn.Read(buffer)
	if err != nil {
		fmt.Printf("failed to read: %v", err)
	}

	var a, h float64
	_, err = fmt.Sscanf(string(buffer), "%f %f", &a, &h)
	if err != nil {
		return
	}

	fmt.Printf("message: %f %f\n", a, h)

	fmt.Println("calculating area of parallelogram")

	parallelogramArea(a, h)

	fmt.Println("sending answer to client")

	_, err = conn.Write([]byte(fmt.Sprintf("answer: %f", parallelogramArea(a, h))))
	if err != nil {
		fmt.Printf("failed to write: %v", err)
	}

	fmt.Println("answer sent")
}

func parallelogramArea(a, h float64) float64 {
	return a * h
}
