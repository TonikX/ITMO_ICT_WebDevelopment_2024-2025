package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"net"
	"strings"
	"sync"
	"time"
)

type Client struct {
	Name   string
	Color  string
	Conn   net.Conn
	Reader *bufio.Reader
}

var (
	clients   = make(map[string]Client)
	clientsMu sync.Mutex
	colors    = []string{
		"\033[31m", // Red
		"\033[32m", // Green
		"\033[33m", // Yellow
		"\033[34m", // Blue
		"\033[35m", // Magenta
		"\033[36m", // Cyan
	}
	resetColor = "\033[0m"
)

func isNameTaken(name string) bool {
	clientsMu.Lock()
	defer clientsMu.Unlock()

	_, exists := clients[name]
	return exists
}

func broadcastMessage(senderName, senderColor, message string) {
	clientsMu.Lock()
	defer clientsMu.Unlock()

	for _, client := range clients {
		if client.Name != senderName {
			client.Conn.Write([]byte(senderColor + senderName + ": " + message + resetColor + "\n"))
		}
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()

	reader := bufio.NewReader(conn)
	var name string

	for {
		nameInput, _ := reader.ReadString('\n')
		name = strings.TrimSpace(nameInput)

		if name == "" {
			conn.Write([]byte("Name cannot be empty. Try again.\n"))
			continue
		}

		if isNameTaken(name) {
			conn.Write([]byte("Name is already taken. Choose a different name.\n"))
		} else {
			break
		}
	}

	clientColor := colors[rand.Intn(len(colors))]

	client := Client{
		Name:   name,
		Color:  clientColor,
		Conn:   conn,
		Reader: reader,
	}

	clientsMu.Lock()
	clients[name] = client
	clientsMu.Unlock()

	fmt.Printf("%s has joined the chat\n", name)

	conn.Write([]byte("Welcome to the chat, " + name + "!\n"))
	broadcastMessage("Server", "", name+" has joined the chat!")

	for {
		message, err := reader.ReadString('\n')
		if err != nil {
			break
		}
		message = strings.TrimSpace(message)

		if message != "" {
			broadcastMessage(name, client.Color, message)
		}
	}

	clientsMu.Lock()
	delete(clients, name)
	clientsMu.Unlock()

	broadcastMessage("Server", "", name+" has left the chat")
	fmt.Printf("%s has left the chat\n", name)
}

func main() {
	rand.NewSource(time.Now().UnixNano())
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Error starting server:", err)
		return
	}
	defer listener.Close()

	fmt.Println("Chat server started on port 8080")

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting connection:", err)
			continue
		}
		go handleConnection(conn)
	}
}
