package main

import (
    "testing"
    "net/http"
    "net/http/httptest"
)

func request(t *testing.T, handler func (http.ResponseWriter, *http.Request), method string, path string) *httptest.ResponseRecorder {
    request, err := http.NewRequest(method, path, nil)
    if err != nil {
        t.Fatal(err)
    }

    response := httptest.NewRecorder()
    http.HandlerFunc(handler).ServeHTTP(response, request)
    return response
}

func TestIndexHandler(t *testing.T) {
    response := request(t, IndexHandler, "GET", "/")

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
