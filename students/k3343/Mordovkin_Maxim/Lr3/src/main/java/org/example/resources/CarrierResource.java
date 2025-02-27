package org.example.resources;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.example.entities.Carrier;
import org.example.services.CarrierService;

import java.util.List;

@Path("/carriers")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class CarrierResource {

    @Inject
    CarrierService carrierService;

    @GET
    public List<Carrier> getAll() {
        return carrierService.findAll();
    }

    @POST
    public Response create(Carrier carrier) {
        try {
            Carrier saved = carrierService.create(carrier);
            return Response.ok(saved).build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    @PUT
    @Path("/{id}")
    public Response update(@PathParam("id") Long id, Carrier data) {
        try {
            Carrier updated = carrierService.update(id, data);
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
        carrierService.delete(id);
        return Response.noContent().build();
    }
}
