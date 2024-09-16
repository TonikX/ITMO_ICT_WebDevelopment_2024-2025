package main

import (
	"flag"
	"fmt"
	utils "lab_1"
	"net"
	"net/http"
)

func main() {
	// settings
	logger := utils.NewLogger("client")
	port := flag.String("p", "", "Port of the server")
	requests := flag.Int("n", 100, "Number of requests to send")
	flag.Parse()

	if port == nil || *port == "" {
		logger.LogFatal("must specify a port to connect to")
	}

	// init server
	address, err := net.ResolveUDPAddr(utils.ProtocolUDP, *port)
	if err != nil {
		logger.LogFatal("failed to resolve address: %v", err)
	}

	// listen connection
	connection, err := net.ListenUDP(utils.ProtocolUDP, address)
	if err != nil {
		logger.LogFatal("failed to listen: %v", err)
	}
	logger.LogMessage(http.StatusOK, "server started")

	// close server
	defer func() {
		_ = connection.Close()
		logger.LogMessage(http.StatusOK, "server closed")
	}()

	for i := 0; i < *requests; i++ {
		// listen client
		requestBuffer := make([]byte, 1024)
		_, clientAddress, err := connection.ReadFromUDP(requestBuffer)
		if err != nil {
			errMsg := fmt.Sprintf("failed to read from UDP: %v\n", err)
			logger.LogMessage(http.StatusInternalServerError, errMsg)
			continue
		}

		logMsg := fmt.Sprintf("recieved client message is: %s", string(requestBuffer))
		logger.LogMessage(http.StatusOK, logMsg)

		// answer to client
		responseBuffer := []byte("Hello, Client!")
		if _, err := connection.WriteToUDP(responseBuffer, clientAddress); err != nil {
			errMsg := fmt.Sprintf("failed to write to UDP address [%s]: %v\n", clientAddress.String(), err)
			logger.LogMessage(http.StatusInternalServerError, errMsg)
			continue
		}
	}
}
