package ru.barkhatnat.cinema.dto.update;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import ru.barkhatnat.cinema.domain.enums.SeatType;

import java.util.UUID;

/**
 * DTO for {@link ru.barkhatnat.cinema.domain.Seat}
 */
public record SeatUpdateDto(
        @NotNull(message = "Row cannot be null")
        UUID rowId,

        @Min(message = "Seat number must be greater than or equal to 1", value = 1)
        Integer number,

        @NotNull(message = "Seat type cannot be null")
        SeatType type) {
}