package main

import (
    "fmt"
    "net/http"
    "google.golang.org/appengine"
)

func init() {
    http.HandleFunc("/", handler)
}

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "a plaintext pastebin service")
}

func main() {
    appengine.Main()
}
