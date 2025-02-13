package org.example.yourapp;

import jakarta.ws.rs.ApplicationPath;
import jakarta.ws.rs.core.Application;
import java.util.Set;
import java.util.HashSet;

import org.example.config.JacksonConfig;
import org.example.controllers.*;
import org.example.filters.CORSFilter;
import org.example.filters.JwtFilter;

@ApplicationPath("/api")
public class YourAppApplication extends Application {

    @Override
    public Set<Class<?>> getClasses() {
        Set<Class<?>> classes = new HashSet<>();
        classes.add(UserController.class);
        classes.add(ProtectedController.class);
        classes.add(CORSFilter.class);
        classes.add(JwtFilter.class);
        classes.add(AssignmentController.class);
        classes.add(SubmissionController.class);
        classes.add(JacksonConfig.class);
        classes.add(PerformanceController.class);

        return classes;
    }
}
