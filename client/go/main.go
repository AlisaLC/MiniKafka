package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	kafka_client "mini_kafka/client"
)

func main() {
	for {
		reader := bufio.NewReader(os.Stdin)
		fmt.Print("CMD: ")
		cmd, _ := reader.ReadString('\n')
		cmd = strings.TrimSpace(strings.ToUpper(cmd))

		switch cmd {
		case "PUSH":
			fmt.Print("KEY: ")
			key, _ := reader.ReadString('\n')
			key = strings.TrimSpace(key)

			fmt.Print("VALUE: ")
			value, _ := reader.ReadString('\n')
			value = strings.TrimSpace(value)

			kafka_client.Push(key, []byte(value))
		case "PULL":
			key, value := kafka_client.Pull()
			fmt.Printf("key: %s, value: %s\n", key, string(value))
		default:
			fmt.Println("unknown command")
		}
	}
}
