package ru.barkhatnat.cinema.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.cinema.domain.security.LoginRequest;
import ru.barkhatnat.cinema.domain.security.LoginResponse;
import ru.barkhatnat.cinema.dto.create.UserCreateDto;
import ru.barkhatnat.cinema.dto.regular.UserDto;
import ru.barkhatnat.cinema.security.CustomUserDetails;
import ru.barkhatnat.cinema.security.JwtIssuer;
import ru.barkhatnat.cinema.service.UserService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/auth")
@Tag(name = "Authentication", description = "API для регистрации и авторизации пользователей")
public class AuthController {

    private final JwtIssuer jwtIssuer;
    private final AuthenticationManager authenticationManager;
    private final UserService userService;

    @PostMapping("/registration")
    @Operation(
            summary = "Регистрация пользователя",
            description = "Создает нового пользователя на основе предоставленных данных",
            responses = {
                    @ApiResponse(responseCode = "201", description = "Пользователь успешно зарегистрирован")
            })
    public ResponseEntity<UserDto> createAccount(@Valid @RequestBody UserCreateDto userCreateDto) {
        UserDto userResponseDto = userService.create(userCreateDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(userResponseDto);
    }

    @PostMapping("/login")
    @Operation(
            summary = "Авторизация пользователя",
            description = "Аутентифицирует пользователя и возвращает токен доступа",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Авторизация успешна, токен выдан"),
                    @ApiResponse(responseCode = "401", description = "Неверные учетные данные")
            })
    public LoginResponse login(@Valid @RequestBody LoginRequest request) {
        var auth = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword())
        );
        SecurityContextHolder.getContext().setAuthentication(auth);
        CustomUserDetails customUserDetails = (CustomUserDetails) auth.getPrincipal();
        List<String> roles = customUserDetails.getAuthorities().stream().map(GrantedAuthority::getAuthority).toList();
        String token = jwtIssuer.issue(customUserDetails.getUser().getId(), customUserDetails.getUser().getEmail(), roles);
        return LoginResponse.builder().accessToken(token).build();
    }
}
