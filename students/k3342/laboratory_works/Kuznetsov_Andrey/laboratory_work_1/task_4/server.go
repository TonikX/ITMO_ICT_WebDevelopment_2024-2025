package main

import (
	"bufio"
	"flag"
	"fmt"
	utils "lab_1"
	"net"
	"net/http"
	"strings"
	"sync"
)

var (
	messages = make(chan string)
	clients  = make(map[net.Conn]string)
	mu       sync.Mutex
)

func broadcastMessages(logger *utils.Logger) {
	for msg := range messages {
		logger.LogMessage(http.StatusOK, fmt.Sprintf("broadcasting message: %s", msg))

		for conn := range clients {
			if name := clients[conn]; !strings.Contains(msg, fmt.Sprintf("[%s]", name)) {
				_, err := conn.Write([]byte(msg + "\n"))

				if err != nil {
					logMsg := fmt.Sprintf("failed to send message to %s: %v", clients[conn], err)
					logger.LogMessage(http.StatusInternalServerError, logMsg)

					_ = conn.Close()
					mu.Lock()
					delete(clients, conn)
					mu.Unlock()
					return
				}
			}
		}
		logger.LogMessage(http.StatusOK, "message was sent to everyone")
	}
}

func exitConnection(err error, conn net.Conn, logger *utils.Logger) bool {
	if err != nil {
		if err.Error() == "EOF" {
			errorMsg := fmt.Sprintf("%s disconnected", clients[conn])
			logger.LogMessage(http.StatusServiceUnavailable, errorMsg)
			return true
		}
		logger.LogMessage(http.StatusInternalServerError, err.Error())
		return true
	}
	return false
}

func handleConnection(conn net.Conn, logger *utils.Logger) {
	// close connection
	defer func() {
		mu.Lock()
		delete(clients, conn)
		mu.Unlock()
		_ = conn.Close()
		logger.LogMessage(http.StatusOK, "connection closed")
	}()

	// login
	reader := bufio.NewReader(conn)
	name, err := reader.ReadString('\n')
	name = strings.TrimSpace(name)
	if exitConnection(err, conn, logger) {
		return
	}

	// register user
	mu.Lock()
	clients[conn] = name
	mu.Unlock()

	joinChatMsg := fmt.Sprintf("%s joined the chat", name)
	logger.LogMessage(http.StatusOK, joinChatMsg)
	messages <- joinChatMsg

	for {
		// read user messages
		userMessage, err := reader.ReadString('\n')
		if exitConnection(err, conn, logger) {
			exitChatMsg := fmt.Sprintf("%s left the chat", name)
			logger.LogMessage(http.StatusOK, exitChatMsg)
			messages <- exitChatMsg
			break
		}

		userMessage = fmt.Sprintf("[%s] %s", name, strings.TrimSpace(userMessage))
		logger.LogMessage(http.StatusOK, fmt.Sprintf("Sending message to channel: %s", userMessage))
		messages <- userMessage
	}

	// delete user after exit
	mu.Lock()
	delete(clients, conn)
	mu.Unlock()
}

func main() {
	// settings
	logger := utils.NewLogger("server")
	port := flag.String("p", "", "Port of the server")
	flag.Parse()

	if port == nil || *port == "" {
		logger.LogFatal("must specify a port to connect to")
	}

	// init server
	listener, err := net.Listen(utils.ProtocolTCP, *port)
	if err != nil {
		logger.LogFatal("failed to listen: %v", err)
	}
	logger.LogMessage(http.StatusOK, "server started")

	// close listener
	defer func() {
		_ = listener.Close()
		logger.LogMessage(http.StatusOK, "server closed")
	}()

	go broadcastMessages(logger)

	for {
		// accept connection
		connection, err := listener.Accept()
		if err != nil {
			errorMsg := fmt.Sprintf("failed to accept connection: %v", err)
			logger.LogMessage(http.StatusInternalServerError, errorMsg)
			continue
		}

		go handleConnection(connection, logger)
	}
}
