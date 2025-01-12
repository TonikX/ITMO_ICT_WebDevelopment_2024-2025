package ru.barkhatnat.cinema.domain.security;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class LoginResponse {
    private final String accessToken;
}
