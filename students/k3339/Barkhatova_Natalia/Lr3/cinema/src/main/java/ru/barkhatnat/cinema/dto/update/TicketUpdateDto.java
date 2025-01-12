package ru.barkhatnat.cinema.dto.update;

import jakarta.validation.constraints.NotNull;

import java.util.UUID;

/**
 * DTO for {@link ru.barkhatnat.cinema.domain.Ticket}
 */
public record TicketUpdateDto(
        @NotNull(message = "User cannot be null")
        UUID userId,

        @NotNull(message = "Session cannot be null")
        UUID sessionId,

        @NotNull(message = "Seat cannot be null")
        UUID seatId) {
}