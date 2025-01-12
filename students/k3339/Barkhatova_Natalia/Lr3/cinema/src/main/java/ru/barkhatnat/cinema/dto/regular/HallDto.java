package ru.barkhatnat.cinema.dto.regular;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import java.util.List;
import java.util.UUID;

/**
 * DTO for {@link ru.barkhatnat.cinema.domain.Hall}
 */
public record HallDto(
        UUID id,

        @Size(message = "Hall name should not exceed 32 characters", max = 32)
        @NotBlank(message = "Hall name cannot be blank")
        String name,

        @Min(message = "Capacity cannot be negative", value = 0)
        Integer capacity,

        List<RowDto> rows,

        List<SessionDto> sessions) {
}