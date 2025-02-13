package org.example.controllers;

import org.example.services.UserService;
import org.example.entities.User;
import org.example.security.JwtUtil;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import java.util.Map;

@Path("/users")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class UserController {

    @Inject
    private UserService userService;

    @Inject
    private JwtUtil jwtUtil;

    // Endpoint для регистрации
    @POST
    @Path("/register")
    public Response register(User user) {
        String username = user.getUsername();
        String password = user.getPassword();
        String role = user.getRole();

        if (username == null || password == null) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity(Map.of("message", "Username and password are required"))
                    .build();
        }

        // Если роль не передали, назначим "Student" по умолчанию
        if (role == null || role.isEmpty()) {
            role = "Student";
            user.setRole(role);
        }

        // Если ученик — нужно проверить classNumber
        if ("Student".equalsIgnoreCase(role)) {
            Integer classNumber = user.getClassNumber();
            // Если с фронта не передаётся, можно потребовать заполнения
            if (classNumber == null || classNumber < 1 || classNumber > 11) {
                return Response.status(Response.Status.BAD_REQUEST)
                        .entity(Map.of("message", "classNumber must be in range 1..11"))
                        .build();
            }
        }

        boolean success = userService.register(user);
        if (success) {
            return Response.status(Response.Status.CREATED)
                    .entity(Map.of("message", "User registered successfully", "role", role))
                    .build();
        } else {
            return Response.status(Response.Status.CONFLICT)
                    .entity(Map.of("message", "Username already exists"))
                    .build();
        }
    }

    // Endpoint для аутентификации
    @POST
    @Path("/login")
    public Response login(User user) {
        String username = user.getUsername();
        String password = user.getPassword();

        if (username == null || password == null) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity(Map.of("message", "Username and password are required"))
                    .build();
        }

        boolean authenticated = userService.authenticate(username, password);
        if (authenticated) {
            String token = jwtUtil.generateToken(username);
            // Возвращаем и роль
            User foundUser = userService.findByUsername(username);
            String role = foundUser.getRole();

            return Response.ok(Map.of(
                    "message", "Login successful",
                    "token", token,
                    "role", role
            )).build();
        } else {
            return Response.status(Response.Status.UNAUTHORIZED)
                    .entity(Map.of("message", "Invalid username or password"))
                    .build();
        }
    }
}
