package main

import (
	"fmt"
	"io"
	"math/cmplx"
	"net"
	"strconv"
	"strings"
)

func Solve(a, b, c complex128) (xpos, xneg complex128) {
	negB := -b
	twoA := 2 * a
	bSquared := b * b
	fourAC := 4 * a * c
	discrim := bSquared - fourAC
	sq := cmplx.Sqrt(discrim)
	xpos = (negB + sq) / twoA
	xneg = (negB - sq) / twoA
	return
}

func sendResponse(conn net.Conn, xpos, xneg complex128) {
	_, err := conn.Write([]byte(fmt.Sprintf("x1 = %v, x2 = %v\n", xpos, xneg)))
	if err != nil {
		fmt.Printf("Couldn't send response %v", err)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()

	p := make([]byte, 2048)
	for {
		n, err := conn.Read(p)
		if err != nil {
			if err == io.EOF {
				return
			}
			fmt.Printf("Error reading from connection: %v\n", err)
			return
		}

		message := string(p[:n])
		fmt.Printf("Received message: %s\n", message)

		// Разбор строки на числа
		parts := strings.Fields(message) // Разделяем строку на части
		if len(parts) != 3 {
			fmt.Println("Expected 3 numbers.")
			continue
		}

		// Преобразование строк в числа
		a, err := strconv.ParseFloat(parts[0], 64)
		if err != nil {
			fmt.Printf("Error parsing a: %v\n", err)
			continue
		}
		b, err := strconv.ParseFloat(parts[1], 64)
		if err != nil {
			fmt.Printf("Error parsing b: %v\n", err)
			continue
		}
		c, err := strconv.ParseFloat(parts[2], 64)
		if err != nil {
			fmt.Printf("Error parsing c: %v\n", err)
			continue
		}

		// Преобразуем в комплексные числа
		xpos, xneg := Solve(complex(a, 0), complex(b, 0), complex(c, 0))
		sendResponse(conn, xpos, xneg)
	}
}

func main() {
	// Listen on TCP port 1234
	ln, err := net.Listen("tcp", ":1234")
	if err != nil {
		fmt.Printf("Error starting TCP server: %v\n", err)
		return
	}
	defer ln.Close()

	fmt.Println("Listening on port 1234...")

	for {
		conn, err := ln.Accept()
		if err != nil {

			fmt.Printf("Error accepting connection: %v\n", err)
			continue
		}

		go handleConnection(conn)
	}
}
