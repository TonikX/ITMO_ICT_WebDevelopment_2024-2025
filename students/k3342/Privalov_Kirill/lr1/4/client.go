package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

func init() {
	fmt.Println("Enter your name.")
}

func main() {
	conn, err := net.Dial("tcp", "localhost:8080")
	if err != nil {
		fmt.Println("Error connecting to server:", err)
		return
	}
	defer conn.Close()

	go func() {
		reader := bufio.NewReader(conn)
		for {
			message, err := reader.ReadString('\n')
			if err != nil {
				fmt.Println("Disconnected from server")
				return
			}
			fmt.Print(message)
		}
	}()

	writer := bufio.NewWriter(conn)
	scanner := bufio.NewScanner(os.Stdin)

	for scanner.Scan() {
		message := scanner.Text()
		message = strings.TrimSpace(message)
		if message != "" {
			writer.WriteString(message + "\n")
			writer.Flush()
		}
	}
}
