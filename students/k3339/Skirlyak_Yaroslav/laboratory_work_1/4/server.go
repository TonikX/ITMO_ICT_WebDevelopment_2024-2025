package main

import (
	"bufio"
	"fmt"
	"net"
	"sync"
)

var (
	clients   = make(map[net.Conn]bool)
	mu        sync.Mutex
	broadcast = make(chan string)
)

func handleClient(conn net.Conn) {
	defer func() {
		mu.Lock()
		delete(clients, conn)
		mu.Unlock()
		conn.Close()
		fmt.Printf("client disconnected from %s\n", conn.RemoteAddr().String())
	}()

	reader := bufio.NewReader(conn)
	for {
		message, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("error reading message:", err)
			return
		}

		fmt.Printf("message recived: %s", message)
		broadcast <- message
	}
}

func broadcaster() {
	for {
		message := <-broadcast
		fmt.Printf("broadcasting message: %s", message)

		mu.Lock()
		for client := range clients {
			_, err := client.Write([]byte(message))
			if err != nil {
				fmt.Println("error sending message:", err)
				client.Close()
				delete(clients, client)
			}
		}
		mu.Unlock()
	}
}

func main() {
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		panic(err)
	}
	defer listener.Close()

	go broadcaster()

	fmt.Println("chat started")

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("error accepting connection:", err)
			continue
		}

		fmt.Printf("new client connected: %s\n", conn.RemoteAddr())

		mu.Lock()
		clients[conn] = true
		mu.Unlock()

		go handleClient(conn)
	}
}
