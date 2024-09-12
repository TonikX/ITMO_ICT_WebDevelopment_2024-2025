package main

import (
	"bufio"
	"flag"
	"fmt"
	utils "lab_1"
	"net"
	"net/http"
	"os"
	"strings"
)

func readServerMessages(conn net.Conn, logger *utils.Logger) {
	reader := bufio.NewReader(conn)
	for {
		serverMessage, _ := reader.ReadString('\n')
		serverMessage = strings.TrimSpace(serverMessage)
		logger.LogMessage(http.StatusOK, serverMessage)
	}
}

func main() {
	// settings
	logger := utils.NewLogger("client")
	port := flag.String("p", "", "Port of the server")
	flag.Parse()

	if port == nil || *port == "" {
		logger.LogFatal("must specify a port to connect to")
	}

	// init client
	connection, err := net.Dial(utils.ProtocolTCP, utils.Localhost+*port)
	if err != nil {
		logger.LogFatal("failed to dial: %v", err)
	}
	logger.LogMessage(http.StatusOK, "client started")

	// register
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Enter your name: ")
	name, _ := reader.ReadString('\n')
	_, _ = connection.Write([]byte(name))

	go readServerMessages(connection, logger)

	for {
		// reading stdin
		message, _ := reader.ReadString('\n')

		// close client
		if strings.TrimSpace(message) == "exit" {
			_ = connection.Close()
			logger.LogMessage(http.StatusOK, "client closed")
			break
		}

		// write to server
		if _, err := connection.Write([]byte(message)); err != nil {
			errorMsg := fmt.Sprintf("failed to write to server: %v", err)
			logger.LogMessage(http.StatusInternalServerError, errorMsg)
		}
	}
}
