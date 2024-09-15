package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
)

func main() {
	tcpAddr, err := net.ResolveTCPAddr("tcp", ":8080")
	if err != nil {
		log.Fatalf("[server][ResolveTCPAddr]: %v", err)
	}

	listener, err := net.ListenTCP("tcp", tcpAddr)
	if err != nil {
		log.Fatalf("[server][ListenTCP]: %v", err)
	}
	defer listener.Close()

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("[server][Accept]: %v", err)
			continue
		}

		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()

	data, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		log.Printf("[server][ReadString]: %v", err)
		return
	}

	result, err := handleParams(data)
	if err != nil {
		log.Printf("[server][handleParams]: %v", err)
		return
	}

	_, err = conn.Write([]byte(fmt.Sprintf("%d", result)))
	if err != nil {
		log.Printf("[server][Write]: %v", err)
	}
}

func handleParams(params string) (uint, error) {
	if params == "" {
		return 0, fmt.Errorf("empty params")
	}

	var a, b uint
	_, err := fmt.Sscanf(params, "%d, %d", &a, &b)
	if err != nil {
		return 0, fmt.Errorf("invalid params: %v", err)
	}
	fmt.Println(a, b)

	return a * b, nil
}
