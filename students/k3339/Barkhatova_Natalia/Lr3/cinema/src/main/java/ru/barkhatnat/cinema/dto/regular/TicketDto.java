package ru.barkhatnat.cinema.dto.regular;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import ru.barkhatnat.cinema.domain.enums.TicketStatus;

import java.time.LocalDateTime;
import java.util.UUID;

/**
 * DTO for {@link ru.barkhatnat.cinema.domain.Ticket}
 */
public record TicketDto(
        UUID id,
        @NotNull(message = "User cannot be null")
        UserDto user,

        @NotNull(message = "Session cannot be null")
        SessionDto session,

        @NotNull(message = "Seat cannot be null")
        SeatDto seat,

        @NotNull(message = "Purchased date cannot be null")
        LocalDateTime purchasedAt,

        @Size(message = "Ticket code must be at most 10 characters", max = 10)
        @NotBlank(message = "Ticket code cannot be blank")
        String ticketCode,

        @NotNull(message = "Ticket status cannot be null")
        TicketStatus status) {
}