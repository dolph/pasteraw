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
    fmt.Fprint(w, "Hello, world!")
}

func main() {
    appengine.Main()
}
