package org.example.resources;

import org.example.services.UserService;
import org.example.entities.User;
import org.example.security.JwtUtil;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

@Path("/users")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class UserResource {

    @Inject
    private UserService userService;

    @Inject
    private JwtUtil jwtUtil;

    @POST
    @Path("/register")
    public Response register(User user) {
        boolean success = userService.register(user);
        if (success) {
            return Response.status(Response.Status.CREATED).build();
        } else {
            return Response.status(Response.Status.CONFLICT)
                    .entity("Username already taken")
                    .build();
        }
    }

    @POST
    @Path("/login")
    public Response login(User user) {
        boolean authenticated = userService.authenticate(user.getUsername(), user.getPassword());
        if (authenticated) {
            String token = jwtUtil.generateToken(user.getUsername());
            return Response.ok()
                    .entity("{\"token\":\"" + token + "\"}")
                    .build();
        } else {
            return Response.status(Response.Status.UNAUTHORIZED)
                    .entity("Invalid username or password")
                    .build();
        }
    }
}
