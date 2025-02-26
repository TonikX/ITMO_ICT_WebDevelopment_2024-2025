package org.example.resources;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import org.example.services.AuthService;
import org.example.entities.AppUser;
import org.example.utils.JwtUtils;

/**

 Request Body (JSON):
 {
 "username": "строка",
 "password": "строка",
 "role": "строка"
 }

 */



@Path("/auth")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AuthResource {

    @Inject
    private AuthService authService;

    /**
     * DTO для запроса при регистрации/логине
     */
    public static class AuthRequest {
        public String username;
        public String password;
        public String role;  // можно использовать при регистрации
    }

    /**
     * Регистрация нового пользователя
     */
    @POST
    @Path("/register")
    public Response register(AuthRequest request) {
        try {
            String token = authService.registerUser(request.username, request.password, request.role);
            return Response.ok("{\"token\":\"" + token + "\"}").build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    /**
     * Логин (авторизация) пользователя
     * Request Body (JSON):
     * {
     *   "username": "строка",
     *   "password": "строка"
     * }
     */

    @POST
    @Path("/login")
    public Response login(AuthRequest request) {
        try {
            String token = authService.login(request.username, request.password);
            return Response.ok("{\"token\":\"" + token + "\"}").build();
        } catch (Exception e) {
            return Response.status(Response.Status.UNAUTHORIZED)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    /**
     * Получить данные о текущем пользователе (по JWT)
     * Request Body:
     * {
     *   "userId": 1,
     *   "username": "newuser",
     *   "passwordHash": "...",
     *   "role": "USER"
     * }
     */
    @GET
    @Path("/me")
    public Response getCurrentUser(@HeaderParam("Authorization") String authHeader) {
        // Обычно авторизация приходит в виде "Bearer <token>"
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            return Response.status(Response.Status.UNAUTHORIZED).build();
        }
        String token = authHeader.substring("Bearer ".length());

        // Валидируем токен
        String username = JwtUtils.validateToken(token);
        if (username == null) {
            return Response.status(Response.Status.UNAUTHORIZED).build();
        }

        // Ищем пользователя
        AppUser user = authService.findByUsername(username);
        if (user == null) {
            return Response.status(Response.Status.UNAUTHORIZED).build();
        }

        // Возвращаем JSON с данными пользователя
        return Response.ok(user).build();
    }
}
