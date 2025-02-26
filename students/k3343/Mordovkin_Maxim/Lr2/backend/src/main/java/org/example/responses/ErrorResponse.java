package org.example.responses;

import lombok.Getter;

@Getter
public class ErrorResponse {
    private String error;

    public ErrorResponse() {}

    public ErrorResponse(String error) {
        this.error = error;
    }

    public void setError(String error) {
        this.error = error;
    }
}
