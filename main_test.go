package main

import (
    "testing"
    "net/http"
    "net/http/httptest"
)

func TestIndexHandler(t *testing.T) {
    request, err := http.NewRequest("GET", "/", nil)
    if err != nil {
        t.Fatal(err)
    }

    response := httptest.NewRecorder()
    http.HandlerFunc(IndexHandler).ServeHTTP(response, request)

    if status := response.Code; status != http.StatusOK {
        t.Errorf(
            "Handler returned wrong status code: got %v want %v",
            status, http.StatusOK)
    }

    expected_body := "a plaintext pastebin service"
    if response.Body.String() != expected_body {
        t.Errorf(
            "Handler returned unexpected body: got %v want %v",
            response.Body.String(), expected_body)
    }
}
