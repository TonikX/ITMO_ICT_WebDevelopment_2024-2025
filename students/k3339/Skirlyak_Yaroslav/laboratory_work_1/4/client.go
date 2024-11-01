package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {
	conn, err := net.Dial("tcp", "localhost:8080")
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	go func() {
		serverReader := bufio.NewReader(conn)
		for {
			message, _ := serverReader.ReadString('\n')
			fmt.Print(message)
		}
	}()

	reader := bufio.NewReader(os.Stdin)

	for {
		message, _ := reader.ReadString('\n')
		conn.Write([]byte(message))
	}
}
