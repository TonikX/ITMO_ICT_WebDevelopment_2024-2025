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

	for {
		// reading stdin
		reader := bufio.NewReader(os.Stdin)
		fmt.Println("Enter equation or type 'exit' to quit: ")
		message, _ := reader.ReadString('\n')
		message = strings.TrimSpace(message)

		// close client
		if strings.TrimSpace(message) == "exit" {
			_ = connection.Close()
			logger.LogMessage(http.StatusOK, "client closed")
			break
		}

		// write to server
		_, _ = connection.Write([]byte(message + "\n"))

		// read answer
		responseBuffer := make([]byte, 1024)
		_, _ = connection.Read(responseBuffer)
		logger.LogMessage(http.StatusOK, string(responseBuffer))
	}
}
