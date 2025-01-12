package ru.barkhatnat.cinema.dto.update;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

/**
 * DTO for {@link ru.barkhatnat.cinema.domain.Row}
 */
public record RowUpdateDto(
        @Min(message = "Row number must be greater than or equal to 1", value = 1)
        Integer number,

        @NotNull(message = "Hall cannot be null")
        UUID hallId) {
}