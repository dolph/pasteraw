package main

import (
    "testing"
    "net/http"
    "net/http/httptest"
)

type TestHandler struct {
    t *testing.T
    f func (http.ResponseWriter, *http.Request)
}

func (handler TestHandler) request(method string, path string) *httptest.ResponseRecorder {
    request, err := http.NewRequest(method, path, nil)
    if err != nil {
        handler.t.Fatal(err)
    }

    response := httptest.NewRecorder()
    http.HandlerFunc(handler.f).ServeHTTP(response, request)
    return response
}

func (handler TestHandler) GET(path string) *httptest.ResponseRecorder {
    return handler.request("GET", path)
}

func (handler TestHandler) POST(path string) *httptest.ResponseRecorder {
    return handler.request("POST", path)
}

func TestIndexHandler(t *testing.T) {
    handler := TestHandler{t, IndexHandler}
    response := handler.GET("/")

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
