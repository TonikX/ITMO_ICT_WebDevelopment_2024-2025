package org.example.providers;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import jakarta.ws.rs.ext.ContextResolver;
import jakarta.ws.rs.ext.Provider;

/**
 * Кастомный провайдер, регистрирующий JavaTimeModule
 * чтобы LocalDateTime и т.п. корректно десериализовывались
 */
@Provider
public class ObjectMapperContextResolver implements ContextResolver<ObjectMapper> {

    private final ObjectMapper mapper;

    public ObjectMapperContextResolver() {
        mapper = new ObjectMapper();
        // ВАЖНО: регистрируем модуль
        mapper.registerModule(new JavaTimeModule());

    }

    @Override
    public ObjectMapper getContext(Class<?> type) {
        return mapper;
    }
}
