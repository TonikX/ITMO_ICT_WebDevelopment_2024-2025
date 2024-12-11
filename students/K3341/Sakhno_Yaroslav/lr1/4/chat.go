package main

import (
	"bufio"
	"net"
	"sync"

	"github.com/google/uuid"
	"go.uber.org/zap"
)

func main() {
	var loggerConfig = zap.NewProductionConfig()
	loggerConfig.Level.SetLevel(zap.DebugLevel)

	logger, err := loggerConfig.Build()
	if err != nil {
		panic(err)
	}

	l, err := net.Listen("tcp", "localhost:9090")
	if err != nil {
		return
	}

	defer l.Close()

	var connMap = &sync.Map{}

	for {
		conn, err := l.Accept()
		if err != nil {
			logger.Error("error accepting connection", zap.Error(err))
			return
		}

		id := uuid.New().String()
		connMap.Store(id, conn)

		go handleUserConnection(id, conn, connMap, logger)
	}
}

func handleUserConnection(id string, c net.Conn, connMap *sync.Map, logger *zap.Logger) {
	defer func() {
		c.Close()
		connMap.Delete(id)
	}()

	for {
		userInput, err := bufio.NewReader(c).ReadString('\n')
		if err != nil {
			logger.Error("error reading from client", zap.Error(err))
			return
		}

		connMap.Range(func(key, value interface{}) bool {
			if conn, ok := value.(net.Conn); ok {
				if _, err := conn.Write([]byte(userInput)); err != nil {
					logger.Error("error accepting connection", zap.Error(err))
				}
			}

			return true
		})
	}
}
