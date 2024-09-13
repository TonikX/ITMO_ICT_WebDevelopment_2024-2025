package lab_1

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

const (
	Localhost   = "localhost"
	ProtocolUDP = "udp"
	ProtocolTCP = "tcp"
)

type Logger struct {
	log *log.Logger
}

func NewLogger(instance string) *Logger {
	instance = fmt.Sprintf("[%s] ", instance)
	logger := log.New(os.Stdout, instance, log.LstdFlags|log.Lmicroseconds)
	return &Logger{logger}
}

func (l *Logger) LogMessage(status int, message string) {
	statusMessage := "SUCCESS"
	if !(200 <= status && status < 300) {
		statusMessage = "ERROR"
	}
	l.log.Printf("[%s %d] %s\n", statusMessage, status, message)
}

func (l *Logger) LogFatal(message string, args ...interface{}) {
	statusMessage := "ERROR"
	status := http.StatusInternalServerError
	l.log.Fatalf("[%s %d] %s\n", statusMessage, status, fmt.Sprintf(message, args...))
}
