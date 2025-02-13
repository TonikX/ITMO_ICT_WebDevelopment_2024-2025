package org.example.controllers;

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import java.util.Map;

@Path("/protected")
@Produces(MediaType.APPLICATION_JSON)
public class ProtectedController {

    @GET
    public Response getProtectedData() {
        return Response.ok(Map.of("message", "This is protected data")).build();
    }
}
