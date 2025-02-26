// src/main/java/org/example/resources/CrewMemberResource.java
package org.example.resources;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.example.entities.CrewMember;
import org.example.services.CrewMemberService;

import java.util.List;

@Path("/crew-members")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class CrewMemberResource {

    @Inject
    private CrewMemberService crewMemberService;

    @GET
    public List<CrewMember> getAllCrewMembers() {
        return crewMemberService.findAll();
    }

    @POST
    public Response createCrewMember(CrewMember crewMember) {
        try {
            CrewMember saved = crewMemberService.create(crewMember);
            return Response.ok(saved).build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    @PUT
    @Path("/{id}")
    public Response updateCrewMember(@PathParam("id") Long id, CrewMember data) {
        try {
            CrewMember updated = crewMemberService.update(id, data);
            return Response.ok(updated).build();
        } catch (Exception e) {
            return Response.status(Response.Status.NOT_FOUND)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    @DELETE
    @Path("/{id}")
    public Response deleteCrewMember(@PathParam("id") Long id) {
        crewMemberService.delete(id);
        return Response.noContent().build();
    }

    @GET
    @Path("/{id}")
    public Response getCrewMemberById(@PathParam("id") Long id) {
        CrewMember crewMember = crewMemberService.findById(id);
        if (crewMember == null) {
            return Response.status(Response.Status.NOT_FOUND)
                    .entity("{\"error\":\"CrewMember not found\"}")
                    .build();
        }
        return Response.ok(crewMember).build();
    }

    @POST
    @Path("/{id}/assign-flight/{flightId}")
    public Response assignToFlight(@PathParam("id") Long id, @PathParam("flightId") Long flightId) {
        try {
            CrewMember updated = crewMemberService.assignToFlight(id, flightId);
            return Response.ok(updated).build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    @POST
    @Path("/{id}/remove-flight")
    public Response removeFromFlight(@PathParam("id") Long id) {
        try {
            CrewMember updated = crewMemberService.removeFromFlight(id);
            return Response.ok(updated).build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }
}
