package org.example.resources;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.example.entities.AircraftMaintenance;
import org.example.services.AircraftMaintenanceService;

import java.util.List;

@Path("/aircraft-maintenances")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AircraftMaintenanceResource {

    @Inject
    private AircraftMaintenanceService maintenanceService;

    @GET
    public List<AircraftMaintenance> getAllMaintenances() {
        return maintenanceService.findAll();
    }

    @POST
    public Response createMaintenance(AircraftMaintenance maintenance) {
        try {
            AircraftMaintenance saved = maintenanceService.create(maintenance);
            return Response.ok(saved).build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    @PUT
    @Path("/{id}")
    public Response updateMaintenance(@PathParam("id") Long id, AircraftMaintenance data) {
        try {
            AircraftMaintenance updated = maintenanceService.update(id, data);
            return Response.ok(updated).build();
        } catch (Exception e) {
            return Response.status(Response.Status.NOT_FOUND)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    @DELETE
    @Path("/{id}")
    public Response deleteMaintenance(@PathParam("id") Long id) {
        maintenanceService.delete(id);
        return Response.noContent().build();
    }

    @GET
    @Path("/aircraft/{aircraftId}")
    public List<AircraftMaintenance> getMaintenancesByAircraft(@PathParam("aircraftId") Long aircraftId) {
        return maintenanceService.findByAircraftId(aircraftId);
    }
}
