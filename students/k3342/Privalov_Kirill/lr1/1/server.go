package main

import (
	"fmt"
	"log"
	"net"
)

func main() {
	udpAddr, err := net.ResolveUDPAddr("udp", ":8080")
	if err != nil {
		log.Fatalf("[server][ResolveUDPAddr]: %v", err)
	}

	conn, err := net.ListenUDP("udp", udpAddr)
	if err != nil {
		log.Fatalf("[server][ListenUDP]: %v", err)
	}
	defer conn.Close()

	for {
		var buf [1024]byte
		n, addr, err := conn.ReadFromUDP(buf[0:])
		if err != nil {
			log.Printf("[server][ReadFromUDP]: %v", err)
			return
		}

		message := string(buf[:n])
		fmt.Println(message)

		if message == "Hello, server" {
			_, err = conn.WriteToUDP([]byte("Hello, client"), addr)
			if err != nil {
				log.Printf("[server][WriteToUDP]: %v", err)
				return
			}
		}
	}
}
