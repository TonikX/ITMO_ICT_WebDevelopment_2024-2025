package org.example.controllers;

import org.example.dto.ClassStatsDTO;
import org.example.entities.User;
import org.example.security.JwtUtil;
import org.example.services.PerformanceService;
import org.example.services.UserService;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import java.util.List;
import java.util.Map;

@Path("/performance")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class PerformanceController {

    @Inject
    private JwtUtil jwtUtil;

    @Inject
    private UserService userService;

    @Inject
    private PerformanceService performanceService;

    /**
     * Возвращает список статистики по всем заданиям (title, avgGrade, etc.)
     * для класса, в котором учится текущий пользователь-студент.
     */
    @GET
    @Path("/my-class")
    public Response getClassPerformance(@HeaderParam("Authorization") String authHeader) {
        String username = extractUsernameFromBearer(authHeader);
        if (username == null) {
            // Не удалось извлечь юзернейм из токена
            return Response.status(Response.Status.UNAUTHORIZED).build();
        }

        // Ищем User
        User student = userService.findByUsername(username);
        if (student == null || !"Student".equalsIgnoreCase(student.getRole())) {
            return Response.status(Response.Status.FORBIDDEN)
                    .type(MediaType.APPLICATION_JSON)
                    .entity(Map.of("message", "Only Student can view class performance"))
                    .build();
        }

        if (student.getClassNumber() == null) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .type(MediaType.APPLICATION_JSON)
                    .entity(Map.of("message", "У вас не задан classNumber"))
                    .build();
        }

        // Достаём нужную статистику
        List<ClassStatsDTO> stats = performanceService.getStatsForClass(student.getClassNumber());

        // Возвращаем
        return Response.ok(stats).build();
    }

    /**
     * Пример: извлечь username из Bearer-токена через JwtUtil.
     */
    private String extractUsernameFromBearer(String authHeader) {
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            return null;
        }
        String token = authHeader.substring("Bearer ".length()).trim();
        try {
            return jwtUtil.validateToken(token);
        } catch (Exception e) {
            return null;
        }
    }
}
