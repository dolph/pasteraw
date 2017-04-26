package main

import (
    "testing"
    "net/http"
    "net/http/httptest"
)

type TestHandler struct {
    t *testing.T

    // The HTTP handler function to be tested.
    f func (http.ResponseWriter, *http.Request)
}

// Build an HTTP request, pass it to the HTTP handler, and return the response.
func (handler TestHandler) request(method string, path string, headers map[string]string) *httptest.ResponseRecorder {
    request, err := http.NewRequest(method, path, nil)
    if err != nil {
        handler.t.Fatal(err)
    }

    // Set request headers, if any.
    for header, value := range headers {
        request.Header.Set(header, value)
    }

    response := httptest.NewRecorder()
    http.HandlerFunc(handler.f).ServeHTTP(response, request)
    return response
}

// Make a GET request to the HTTP handler, and return the response.
func (handler TestHandler) GET(path string, headers map[string]string) *httptest.ResponseRecorder {
    return handler.request("GET", path, headers)
}

// Make a POST request to the HTTP handler, and return the response.
func (handler TestHandler) POST(path string, headers map[string]string) *httptest.ResponseRecorder {
    return handler.request("POST", path, headers)
}

func TestIndexHandler(t *testing.T) {
    handler := TestHandler{t, IndexHandler}
    response := handler.GET("/", nil)

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
