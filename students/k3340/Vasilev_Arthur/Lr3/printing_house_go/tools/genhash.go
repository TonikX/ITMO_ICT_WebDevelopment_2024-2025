package main

import (
	"fmt"
	"golang.org/x/crypto/bcrypt"
)

func main() {
	password := "password123"
	
	fmt.Println("Generating 3 different hashes for password:", password)
	fmt.Println()
	
	for i := 1; i <= 3; i++ {
		hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
		if err != nil {
			panic(err)
		}
		
		fmt.Printf("Hash %d (length %d):\n%s\n\n", i, len(hash), string(hash))
		
		// Verify
		err = bcrypt.CompareHashAndPassword(hash, []byte(password))
		if err == nil {
			fmt.Printf("✓ Hash %d verified successfully!\n\n", i)
		} else {
			fmt.Printf("✗ Hash %d verification failed!\n\n", i)
		}
	}
}
