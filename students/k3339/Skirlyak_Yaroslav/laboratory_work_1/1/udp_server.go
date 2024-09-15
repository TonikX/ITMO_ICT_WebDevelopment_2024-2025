package main

import (
	"fmt"
	"net"
)

const (
	serverMessage = "Hello, client"
	port          = 8080
	host          = "127.0.0.1"
)

func main() {
	addr := &net.UDPAddr{
		IP:   net.ParseIP(host),
		Port: port,
	}

	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	fmt.Printf("server started on %s:%d\n", host, port)

	reader := make([]byte, 1024)

	_, addr, err = conn.ReadFromUDP(reader)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Printf("message: %s", reader)
	sendMessage(conn, addr)

}

func sendMessage(conn *net.UDPConn, addr *net.UDPAddr) {
	_, err := conn.WriteTo([]byte(serverMessage), addr)
	if err != nil {
		fmt.Println(err)
	}
}
