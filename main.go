package main

import (
    "fmt"
    "net/http"
    "google.golang.org/appengine"
)

func init() {
    http.HandleFunc("/", IndexHandler)
}

func IndexHandler(w http.ResponseWriter, r *http.Request) {
    switch r.Method {
        case http.MethodGet:
            GetIndex(w, r)
        case http.MethodPost:
            PostIndex(w, r)
        default:
            NotFound(w, r)
    }
}

func GetIndex(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    w.Header().Set("Content-Type", "text/plain")
    fmt.Fprint(w, "a plaintext pastebin service")
}

func PostIndex(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusFound)
    w.Header().Set("Location", "http://cdn.pasteraw.com/")
}

func NotFound(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusNotFound)
    w.Header().Set("Content-Type", "text/plain")
    fmt.Fprintf(w, "%d Not Found", http.StatusNotFound)
}

func main() {
    appengine.Main()
}
