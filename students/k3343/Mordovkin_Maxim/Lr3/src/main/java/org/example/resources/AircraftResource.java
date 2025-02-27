package org.example.resources;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.example.entities.Aircraft;
import org.example.services.AircraftService;

import java.util.List;

@Path("/aircrafts")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AircraftResource {

    @Inject
    AircraftService aircraftService;

    @GET
    public List<Aircraft> getAll() {
        return aircraftService.findAll();
    }

    @POST
    public Response create(Aircraft aircraft) {
        try {
            Aircraft saved = aircraftService.create(aircraft);
            return Response.ok(saved).build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    @PUT
    @Path("/{id}")
    public Response update(@PathParam("id") Long id, Aircraft data) {
        try {
            Aircraft updated = aircraftService.update(id, data);
            return Response.ok(updated).build();
        } catch (Exception e) {
            return Response.status(Response.Status.NOT_FOUND)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    @DELETE
    @Path("/{id}")
    public Response delete(@PathParam("id") Long id) {
        aircraftService.delete(id);
        return Response.noContent().build();
    }
}
