package main

import (
	"flag"
	"fmt"
	"log"
	"net"
)

var a, b uint

func main() {
	tcpAddr, err := net.ResolveTCPAddr("tcp", ":8080")
	if err != nil {
		log.Fatalf("[client][ResolveTCPAddr]: %v", err)
	}

	conn, err := net.DialTCP("tcp", nil, tcpAddr)
	if err != nil {
		log.Fatalf("[client][DialTCP]: %v", err)
	}
	defer conn.Close()

	_, err = conn.Write([]byte(fmt.Sprintf("%d, %d\n", a, b)))
	if err != nil {
		log.Fatalf("[client][Write]: %v", err)
	}

	var buf [1024]byte
	n, err := conn.Read(buf[0:])
	if err != nil {
		log.Fatalf("[client][Read]: %v", err)
	}

	fmt.Println(string(buf[:n]))
}

func init() {
	flag.UintVar(&a, "a", 0, "Parameter a")
	flag.UintVar(&b, "b", 0, "Parameter b")
	flag.Parse()
}
