package client

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"log"
	"net/http"
	nurl "net/url"
	"os"
	"time"

	"github.com/joho/godotenv"
)

var (
	GATEWAY_URL string
	http_client = &http.Client{}
)

func init() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	GATEWAY_URL = "http://" + os.Getenv("GATEWAY_HOST") + ":" + os.Getenv("GATEWAY_PORT")
}

func blockingRequest(method, url string, data []byte, headers map[string]string) []byte {
	for {
		req, err := http.NewRequest(method, url, bytes.NewBuffer(data))
		if err != nil {
			log.Println("Error creating request:", err)
			continue
		}
		for key, value := range headers {
			req.Header.Set(key, value)
		}
		resp, err := http_client.Do(req)
		if err != nil {
			log.Println("Error making request:", err)
			time.Sleep(time.Second)
			continue
		}
		defer resp.Body.Close()
		body := new(bytes.Buffer)
		_, err = body.ReadFrom(resp.Body)
		if err != nil {
			log.Println("Error reading response:", err)
			time.Sleep(time.Second)
			continue
		}
		if resp.StatusCode != 200 {
			log.Println("Error response:", resp.Status, body.String())
			time.Sleep(time.Second)
			continue
		}
		return body.Bytes()
	}
}

func Push(key string, value []byte) {
	url := GATEWAY_URL + "/push"
	encodedValue := base64.StdEncoding.EncodeToString(value)
	logger := log.New(os.Stdout, "", 0)
	logger.Println("Pushing message:", key, encodedValue)

	formData := nurl.Values{}
	formData.Set("key", key)
	formData.Set("value", encodedValue)

	response := blockingRequest("POST", url, []byte(formData.Encode()), map[string]string{"Content-Type": "application/x-www-form-urlencoded"})
	logger.Println("Push response:", string(response))
}

func Pull() (string, []byte) {
	url := GATEWAY_URL + "/pull"
	response := blockingRequest("GET", url, nil, nil)
	logger := log.New(os.Stdout, "", 0)
	logger.Println("Pulled message:", string(response))
	var data map[string]string
	err := json.Unmarshal(response, &data)
	if err != nil {
		log.Println("Error decoding JSON:", err)
		return "", nil
	}
	key := data["key"]
	decodedValue, err := base64.StdEncoding.DecodeString(data["value"])
	if err != nil {
		log.Println("Error decoding base64:", err)
		return "", nil
	}
	return key, decodedValue
}

func Subscribe(f func(string, []byte)) {
	for {
		key, value := Pull()
		f(key, value)
	}
}
