package main

import (
	"fmt"
	"log"
	"net"
)

func main() {
	udpAddr, err := net.ResolveUDPAddr("udp", ":8080")
	if err != nil {
		log.Fatalf("[client][ResolveUDPAddr]: %v", err)
	}

	conn, err := net.DialUDP("udp", nil, udpAddr)
	if err != nil {
		log.Fatalf("[client][DialUDP]: %v", err)
	}
	defer conn.Close()

	_, err = conn.Write([]byte("Hello, server"))
	if err != nil {
		log.Fatalf("[client][Write]: %v", err)
	}

	var buf [1024]byte
	n, _, err := conn.ReadFromUDP(buf[0:])
	if err != nil {
		log.Fatalf("[client][ReadFromUDP]: %v", err)
	}
	fmt.Println(string(buf[:n]))
}
