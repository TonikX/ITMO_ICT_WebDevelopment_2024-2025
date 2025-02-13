package org.example.controllers;

import lombok.Getter;
import org.example.security.JwtUtil;
import org.example.entities.Assignment;
import org.example.entities.Submission;
import org.example.entities.User;
import org.example.services.SubmissionService;
import org.example.services.AssignmentService;
import org.example.services.UserService;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Path("/submissions")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class SubmissionController {

    @Inject
    private SubmissionService submissionService;

    @Inject
    private AssignmentService assignmentService;

    @Inject
    private UserService userService;

    @Inject
    private JwtUtil jwtUtil;

    @POST
    public Response createSubmission(SubmissionRequest dto, @HeaderParam("Authorization") String authHeader) {
        String username = extractUsernameFromBearer(authHeader);
        if (username == null) {
            return Response.status(Response.Status.UNAUTHORIZED).build();
        }

        User student = userService.findByUsername(username);
        if (student == null || !"Student".equalsIgnoreCase(student.getRole())) {
            return Response.status(Response.Status.FORBIDDEN)
                    .entity(Map.of("message", "Only Student can submit assignments"))
                    .build();
        }

        Assignment assignment = assignmentService.getAssignmentById(dto.getAssignmentId());
        if (assignment == null) {
            return Response.status(Response.Status.NOT_FOUND)
                    .entity(Map.of("message", "Assignment not found"))
                    .build();
        }

        LocalDateTime now = LocalDateTime.now();
        if (now.isAfter(assignment.getDueDate())) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity(Map.of("message", "Срок выполнения пропущен!"))
                    .build();
        }

        Submission submission = submissionService.createSubmission(assignment, student, dto.getContent());
        return Response.ok(submission).build();
    }

    @PUT
    @Path("/{submissionId}/grade")
    public Response gradeSubmission(@PathParam("submissionId") Long submissionId,
                                    GradeRequest dto,
                                    @HeaderParam("Authorization") String authHeader) {
        String username = extractUsernameFromBearer(authHeader);
        if (username == null) {
            return Response.status(Response.Status.UNAUTHORIZED).build();
        }

        User teacher = userService.findByUsername(username);
        if (teacher == null || !"Teacher".equalsIgnoreCase(teacher.getRole())) {
            return Response.status(Response.Status.FORBIDDEN)
                    .entity(Map.of("message", "Only Teacher can grade submissions"))
                    .build();
        }

        Submission sub = submissionService.getById(submissionId);
        if (sub == null) {
            return Response.status(Response.Status.NOT_FOUND)
                    .entity(Map.of("message", "Submission not found"))
                    .build();
        }

        Integer grade = dto.getGrade();
        if (grade == null) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity(Map.of("message", "Grade cannot be null"))
                    .build();
        }

        if (grade < 0 || grade > 100) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity(Map.of("message", "Grade must be between 0 and 100"))
                    .build();
        }

        Submission updated = submissionService.setGrade(sub, grade);
        return Response.ok(updated).build();
    }

    @GET
    @Path("/by-assignment/{assignmentId}")
    public Response getSubmissionsByAssignment(@PathParam("assignmentId") Long assignmentId,
                                               @HeaderParam("Authorization") String authHeader) {
        String username = extractUsernameFromBearer(authHeader);
        if (username == null) {
            return Response.status(Response.Status.UNAUTHORIZED).build();
        }
        User teacher = userService.findByUsername(username);
        if (teacher == null || !"Teacher".equalsIgnoreCase(teacher.getRole())) {
            return Response.status(Response.Status.FORBIDDEN)
                    .entity(Map.of("message", "Only Teacher can view all submissions"))
                    .build();
        }

        List<Submission> subs = submissionService.getSubmissionsByAssignment(assignmentId);
        return Response.ok(subs).build();
    }

    @GET
    @Path("/my")
    public Response getMySubmissions(@HeaderParam("Authorization") String authHeader) {
        String username = extractUsernameFromBearer(authHeader);
        if (username == null) {
            return Response.status(Response.Status.UNAUTHORIZED).build();
        }

        User student = userService.findByUsername(username);
        if (student == null || !"Student".equalsIgnoreCase(student.getRole())) {
            return Response.status(Response.Status.FORBIDDEN)
                    .entity(Map.of("message", "Only Student can view their submissions"))
                    .build();
        }

        List<Submission> mySubs = submissionService.getSubmissionsByStudent(student.getId());
        return Response.ok(mySubs).build();
    }

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

    // DTO классы
    @Getter
    public static class SubmissionRequest {
        private Long assignmentId;
        private String content;

        public void setAssignmentId(Long assignmentId) { this.assignmentId = assignmentId; }

        public void setContent(String content) { this.content = content; }
    }

    @Getter
    public static class GradeRequest {
        private Integer grade;

        public void setGrade(Integer grade) { this.grade = grade; }
    }
}
