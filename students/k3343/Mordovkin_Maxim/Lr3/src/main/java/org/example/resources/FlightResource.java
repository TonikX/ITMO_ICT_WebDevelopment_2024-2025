package org.example.resources;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.example.entities.Aircraft;
import org.example.entities.CrewMember;
import org.example.entities.Flight;
import org.example.entities.TransitStop;
import org.example.services.AircraftService;
import org.example.services.CrewMemberService;
import org.example.services.FlightService;
import org.example.services.TransitStopService;

import java.util.List;

@Path("/flights")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class FlightResource {

    @Inject
    private FlightService flightService;

    @Inject
    private AircraftService aircraftService;

    @Inject
    private TransitStopService transitStopService;

    @Inject
    private CrewMemberService crewMemberService;

    @GET
    public Response getAllFlights() {
        List<Flight> flights = flightService.findAll();
        return Response.ok(flights).build();
    }

    @POST
    public Response createFlight(Flight flight) {
        try {
            // Проверка наличия самолёта
            if (flight.getAircraft() != null) {
                Long aircraftId = flight.getAircraft().getAircraftID();
                Aircraft aircraft = aircraftService.findById(aircraftId);
                if (aircraft == null) {
                    return Response.status(Response.Status.BAD_REQUEST)
                            .entity("{\"error\":\"Aircraft not found\"}")
                            .build();
                }
                flight.setAircraft(aircraft);
            }
            Flight created = flightService.createFlight(flight);
            return Response.ok(created).build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    @PUT
    @Path("/{id}")
    public Response updateFlight(@PathParam("id") Long id, Flight flightData) {
        try {
            // Проверка наличия самолёта
            if (flightData.getAircraft() != null) {
                Long aircraftId = flightData.getAircraft().getAircraftID();
                Aircraft aircraft = aircraftService.findById(aircraftId);
                if (aircraft == null) {
                    return Response.status(Response.Status.BAD_REQUEST)
                            .entity("{\"error\":\"Aircraft not found\"}")
                            .build();
                }
                flightData.setAircraft(aircraft);
            }
            Flight updated = flightService.updateFlight(id, flightData);
            return Response.ok(updated).build();
        } catch (Exception e) {
            return Response.status(Response.Status.NOT_FOUND)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    @DELETE
    @Path("/{id}")
    public Response deleteFlight(@PathParam("id") Long id) {
        try {
            flightService.deleteFlight(id);
            return Response.noContent().build();
        } catch (Exception e) {
            return Response.status(Response.Status.NOT_FOUND)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    @GET
    @Path("/{id}")
    public Response getFlightById(@PathParam("id") Long id) {
        Flight flight = flightService.findById(id);
        if (flight == null) {
            return Response.status(Response.Status.NOT_FOUND)
                    .entity("{\"error\":\"Flight not found\"}")
                    .build();
        }
        return Response.ok(flight).build();
    }

    // Управление транзитными посадками

    @POST
    @Path("/{flightId}/transit-stops")
    public Response addTransitStop(@PathParam("flightId") Long flightId, TransitStop transitStop) {
        try {
            TransitStop saved = flightService.addTransitStop(flightId, transitStop);
            return Response.ok(saved).build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    @DELETE
    @Path("/{flightId}/transit-stops/{transitStopId}")
    public Response removeTransitStop(@PathParam("flightId") Long flightId, @PathParam("transitStopId") Long transitStopId) {
        try {
            flightService.removeTransitStop(transitStopId);
            return Response.noContent().build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }

    @GET
    @Path("/{flightId}/transit-stops")
    public Response getTransitStops(@PathParam("flightId") Long flightId) {
        List<TransitStop> stops = transitStopService.findByFlightId(flightId);
        return Response.ok(stops).build();
    }



    @POST
    @Path("/{flightId}/crew-members/{crewMemberId}")
    public Response addCrewMemberToFlight(@PathParam("flightId") Long flightId,
                                          @PathParam("crewMemberId") Long crewMemberId) {
        try {
            CrewMember crewMember = crewMemberService.assignToFlight(crewMemberId, flightId);
            return Response.ok(crewMember).build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }


    @DELETE
    @Path("/{flightId}/crew-members/{crewMemberId}")
    public Response removeCrewMemberFromFlight(@PathParam("flightId") Long flightId, @PathParam("crewMemberId") Long crewMemberId) {
        try {
            CrewMember crewMember = crewMemberService.removeFromFlight(crewMemberId);
            return Response.ok(crewMember).build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity("{\"error\":\"" + e.getMessage() + "\"}")
                    .build();
        }
    }
}


