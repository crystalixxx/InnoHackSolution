package main

import (
	"flag"
	"log"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

var SERVER_URL string

func main() {
	r := gin.New()

	flag.StringVar(&SERVER_URL, "url", "", "url")

	// Set up the webhook endpoint to receive GitLab requests
	r.POST("/gitlab-webhook", handleGitLabWebhookRequest)

	log.Fatal(r.Run(":8080"))
}

func handleGitLabWebhookRequest(c *gin.Context) {
	// Get the request body as JSON
	var gitlabMergeRequest struct {
		ObjectAttributes map[string]interface{} `json:"object_attributes"`
	}

	c.BindJSON(&gitlabMergeRequest)

	// Extract the title and URL from the MR object
	title := gitlabMergeRequest.ObjectAttributes["title"].(string)
	url := gitlabMergeRequest.ObjectAttributes["url"].(string)

	// Parse the tag from the title (assuming it's in the format "tag-name")
	tag := extractTagFromTitle(title)

	// Send the tag and URL to another server using JSON
	sendTagAndUrlToAnotherServer(tag, url)
}

func extractTagFromTitle(title string) string {
	// Implement some more complex logic here
	return strings.Split(title, " ")[0]
}

func sendTagAndUrlToAnotherServer(tag string, url string) {
	// Set up the request to the other server
	// TODO real server adress here
	req, err := http.NewRequest("POST", SERVER_URL,
		strings.NewReader(`{"tag": "`+tag+`", "url": "`+url+`"}`))
	if err != nil {
		log.Println(err)
		return
	}

	// Set the request headers
	req.Header.Set("Content-Type", "application/json")

	// Send the request
	client := &http.Client{}
	_, err = client.Do(req)
	if err != nil {
		log.Println(err)
	}
}
