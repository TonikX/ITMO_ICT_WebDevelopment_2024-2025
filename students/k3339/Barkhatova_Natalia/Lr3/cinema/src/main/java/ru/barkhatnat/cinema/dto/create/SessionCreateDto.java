package ru.barkhatnat.cinema.dto.create;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDateTime;
import java.util.UUID;

/**
 * DTO for {@link ru.barkhatnat.cinema.domain.Session}
 */
public record SessionCreateDto(
        @NotNull(message = "Movie cannot be null")
        UUID movieId,

        @NotNull(message = "Hall cannot be null")
        UUID hallId,

        @NotNull(message = "Start time cannot be null")
        LocalDateTime startTime,

        @Min(message = "Price must be greater than or equal to 0", value = 0)
        Integer price) {
}