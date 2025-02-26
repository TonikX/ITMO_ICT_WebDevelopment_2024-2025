package org.example.resources;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.example.dto.CrewMemberDTO;
import org.example.entities.CrewMember;
import org.example.services.CrewService;
import org.example.util.DTOMapper;

import java.util.List;
import java.util.stream.Collectors;

@Path("/crew")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class CrewResource {

    @Inject
    private CrewService crewService;

    // DTO
    public static class CrewApplyRequest {
        public Long userId;
        public String fullName;
        public int age;
        public String education;
        public int workExperience;
        public String passportData;
        public String role;
    }

    public static class CrewActionRequest {
        public Long crewMemberId; // Изменено на camelCase
    }

    @POST
    @Path("/apply")
    public Response applyForCrew(CrewApplyRequest request) {
        try {
            crewService.applyForCrew(request);
            return Response.ok("{\"success\":true}").build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    /**
     * Получить список PENDING-заявок (для ADMIN)
     */
    @GET
    @Path("/pending")
    public List<CrewMemberDTO> getPendingCrew() {
        return crewService.findPendingCrew().stream()
                .map(DTOMapper::toCrewMemberDTO)
                .collect(Collectors.toList());
    }

    /**
     * Получить все заявки конкретного пользователя
     */
    @GET
    @Path("/my")
    public List<CrewMemberDTO> getMyApplications(@QueryParam("userId") Long userId) {
        return crewService.findByUserId(userId).stream()
                .map(DTOMapper::toCrewMemberDTO)
                .collect(Collectors.toList());
    }

    @POST
    @Path("/approve")
    public Response approveCrew(CrewActionRequest req) {
        try {
            crewService.approveCrew(req.crewMemberId);
            return Response.ok("{\"success\":true}").build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    @POST
    @Path("/reject")
    public Response rejectCrew(CrewActionRequest req) {
        try {
            crewService.rejectCrew(req.crewMemberId);
            return Response.ok("{\"success\":true}").build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }
}

