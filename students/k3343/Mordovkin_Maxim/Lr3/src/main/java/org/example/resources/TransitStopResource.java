package org.example.resources;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.example.entities.TransitStop;
import org.example.services.TransitStopService;

import java.util.Collections;
import java.util.List;

@Path("/transit-stops")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class TransitStopResource {

    @Inject
    private TransitStopService transitStopService;

    @GET
    public List<TransitStop> getAllTransitStops() {
        return transitStopService.findAll();
    }

    @GET
    @Path("/flight/{flightId}")
    public List<TransitStop> getTransitStopsByFlight(@PathParam("flightId") Long flightId) {
        return transitStopService.findByFlightId(flightId);
    }

    @POST
    public Response createTransitStop(TransitStop transitStop) {
        try {
            TransitStop saved = transitStopService.create(transitStop);
            return Response.ok(saved).build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity(Collections.singletonMap("error", e.getMessage()))
                    .build();
        }
    }

    @POST
    @Path("/flight/{flightId}")
    public Response addTransitStopToFlight(@PathParam("flightId") Long flightId, TransitStop transitStop) {
        try {
            TransitStop saved = transitStopService.addTransitStop(flightId, transitStop);
            return Response.ok(saved).build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity(Collections.singletonMap("error", e.getMessage()))
                    .build();
        }
    }

    @DELETE
    @Path("/{id}")
    public Response deleteTransitStop(@PathParam("id") Long id) {
        try {
            transitStopService.delete(id);
            return Response.noContent().build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity(Collections.singletonMap("error", e.getMessage()))
                    .build();
        }
    }
}

