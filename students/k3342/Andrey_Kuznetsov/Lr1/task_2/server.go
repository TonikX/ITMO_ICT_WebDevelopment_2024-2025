package main

import (
	"bufio"
	"flag"
	"fmt"
	utils "lab_1"
	"lab_1/task_2/backend"
	"net"
	"net/http"
)

func handleConnection(conn net.Conn, logger *utils.Logger) {
	// close connection
	defer func() {
		_ = conn.Close()
		logger.LogMessage(http.StatusServiceUnavailable, "connection closed")
	}()

	for {
		message, err := bufio.NewReader(conn).ReadString('\n')
		if err != nil {
			if err.Error() == "EOF" {
				return
			}
			errMsg := fmt.Sprintf("failed to read: %v", err)
			logger.LogMessage(http.StatusInternalServerError, errMsg)
			return
		}

		// solve equation
		coefs, err := backend.ParseString(message)
		if err != nil {
			errorMsg := fmt.Sprintf("failed to parse args: %v", err)
			logger.LogMessage(http.StatusInternalServerError, errorMsg)
			_, _ = conn.Write([]byte(errorMsg))
			continue
		}

		answer := backend.SolveEquation(coefs[0], coefs[1], coefs[2])
		logger.LogMessage(http.StatusOK, "equation is solved!")

		// write to client
		response := []byte(fmt.Sprintf("[solution]: %s", answer))
		_, _ = conn.Write(response)
	}
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

	for {
		// accept connection
		connection, err := listener.Accept()
		if err != nil {
			logMsg := fmt.Sprintf("failed to accept: %v", err)
			logger.LogMessage(http.StatusInternalServerError, logMsg)
			continue
		}

		go handleConnection(connection, logger)
	}
}
