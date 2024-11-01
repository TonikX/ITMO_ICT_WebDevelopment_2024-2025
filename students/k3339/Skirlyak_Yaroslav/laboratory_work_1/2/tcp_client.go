package main

import (
	"fmt"
	"net"
)

func main() {
	conn, err := net.Dial("tcp", "127.0.0.1:8080")
	if err != nil {
		fmt.Printf("failed to listen: %v", err)
	}
	defer conn.Close()

	var a, b int
	fmt.Println("enter 2 nums")
	fmt.Scanf("%d %d", &a, &b)

	for {
		_, err = conn.Write([]byte(fmt.Sprintf("%d %d", a, b)))
		if err != nil {
			fmt.Printf("failed to write: %v", err)
		}

		buffer := make([]byte, 1024)
		_, err = conn.Read(buffer)
		if err != nil {
			fmt.Printf("failed to read: %v", err)
		}

		fmt.Printf("answer: %s", buffer)
	}
}
