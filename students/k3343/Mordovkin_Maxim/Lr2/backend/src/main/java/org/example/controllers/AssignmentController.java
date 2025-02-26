package org.example.controllers;

import org.example.security.JwtUtil; // <-- Нужно импортировать ваш класс
import org.example.entities.Assignment;
import org.example.entities.User;
import org.example.services.AssignmentService;
import org.example.services.UserService;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Path("/assignments")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AssignmentController {

    @Inject
    private AssignmentService assignmentService;

    @Inject
    private UserService userService;

    // Добавьте:
    @Inject
    private JwtUtil jwtUtil;

    @POST
    public Response createAssignment(AssignmentRequest dto, @HeaderParam("Authorization") String authHeader) {
        String username = extractUsernameFromBearer(authHeader);
        if (username == null) {
            return Response.status(Response.Status.UNAUTHORIZED).build();
        }

        User user = userService.findByUsername(username);
        if (user == null || !"Teacher".equalsIgnoreCase(user.getRole())) {
            return Response.status(Response.Status.FORBIDDEN)
                    .entity(Map.of("message", "Only Teacher can create assignments"))
                    .build();
        }

        Assignment assignment = assignmentService.createAssignment(
                dto.getTitle(),
                dto.getDueDate(),
                user
        );

        return Response.status(Response.Status.CREATED).entity(assignment).build();
    }

    @GET
    public Response getAllAssignments() {
        List<Assignment> list = assignmentService.getAllAssignments();
        return Response.ok(list).build();
    }

    private String extractUsernameFromBearer(String authHeader) {
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            return null;
        }
        String token = authHeader.substring("Bearer ".length()).trim();
        try {
            // Вместо JwtHolder -- используем наш jwtUtil:
            return jwtUtil.validateToken(token);
        } catch (Exception e) {
            return null;
        }
    }

    // DTO-класс
    public static class AssignmentRequest {
        private String title;
        private LocalDateTime dueDate;
        // getters/setters
        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }
        public LocalDateTime getDueDate() { return dueDate; }
        public void setDueDate(LocalDateTime dueDate) { this.dueDate = dueDate; }
    }
}
