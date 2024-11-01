package main

import (
	"flag"
	"fmt"
	utils "lab_1"
	"net"
	"net/http"
	"time"
)

func main() {
	// settings
	logger := utils.NewLogger("client")
	port := flag.String("p", "", "Port of the server")
	waitTimeSeconds := flag.Int("s", 3, "Time in seconds between requests")
	requests := flag.Int("n", 100, "Number of requests to send")
	flag.Parse()

	if port == nil || *port == "" {
		logger.LogFatal("must specify a port to connect to")
	}

	// init client
	address, err := net.ResolveUDPAddr(utils.ProtocolUDP, utils.Localhost+*port)
	if err != nil {
		logger.LogFatal("failed to resolve address: %v", err)
	}

	// connect to server
	connection, err := net.DialUDP(utils.ProtocolUDP, nil, address)
	if err != nil {
		logger.LogFatal("could not connect to server: %v", err)
	}
	logger.LogMessage(http.StatusOK, "client started")

	// close client
	defer func() {
		_ = connection.Close()
		logger.LogMessage(http.StatusOK, "client closed")
	}()

	for i := 0; i < *requests; i++ {
		// write to server
		requestBuffer := []byte("Hello, Server!")
		if _, err := connection.Write(requestBuffer); err != nil {
			errorMsg := fmt.Sprintf("failed to write data: %v", err)
			logger.LogMessage(http.StatusInternalServerError, errorMsg)
		}
		time.Sleep(time.Duration(*waitTimeSeconds) * time.Second)

		// listen server
		responseBuffer := make([]byte, 1024)
		if _, err := connection.Read(responseBuffer); err != nil {
			errorMsg := fmt.Sprintf("could not read: %v", err)
			logger.LogMessage(http.StatusInternalServerError, errorMsg)
		}
		logMsg := fmt.Sprintf("recieved server message is: %s", string(responseBuffer))
		logger.LogMessage(http.StatusAccepted, logMsg)
	}
}
