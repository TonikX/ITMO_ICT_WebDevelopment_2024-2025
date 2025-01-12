package ru.barkhatnat.cinema.domain;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.*;
import org.hibernate.annotations.UuidGenerator;
import ru.barkhatnat.cinema.domain.enums.TicketStatus;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Table(
        uniqueConstraints = {
                @UniqueConstraint(name = "uc_session_seat", columnNames = {"session_id", "seat_id"})
        }
)
public class Ticket {
    @Id
    @UuidGenerator
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    @NotNull(message = "User cannot be null")
    private User user;

    @ManyToOne
    @JoinColumn(name = "session_id", nullable = false)
    @NotNull(message = "Session cannot be null")
    private Session session;

    @ManyToOne
    @JoinColumn(name = "seat_id", nullable = false)
    @NotNull(message = "Seat cannot be null")
    private Seat seat;

    @Column(name = "purchased_at", nullable = false)
    @NotNull(message = "Purchased date cannot be null")
    private LocalDateTime purchasedAt;

    @Column(name = "ticket_code", unique = true, nullable = false, length = 10)
    @NotBlank(message = "Ticket code cannot be blank")
    @Size(max = 10, message = "Ticket code must be at most 10 characters")
    private String ticketCode;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    @NotNull(message = "Ticket status cannot be null")
    private TicketStatus status;

    public Ticket(User user, Session session, Seat seat, LocalDateTime purchasedAt, String ticketCode, TicketStatus status) {
        this.user = user;
        this.session = session;
        this.seat = seat;
        this.purchasedAt = purchasedAt;
        this.ticketCode = ticketCode;
        this.status = status;
    }
}