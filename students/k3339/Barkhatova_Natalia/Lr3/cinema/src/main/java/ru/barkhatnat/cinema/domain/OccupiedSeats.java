package ru.barkhatnat.cinema.domain;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import lombok.*;
import org.hibernate.annotations.UuidGenerator;

import java.util.UUID;

@Entity
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class OccupiedSeats {
    @Id
    @UuidGenerator
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "session_id", nullable = false)
    @NotNull(message = "Session cannot be null")
    private Session session;

    @ManyToOne
    @JoinColumn(name = "seat_id", nullable = false)
    @NotNull(message = "Seat cannot be null")
    private Seat seat;

    @Column(nullable = false)
    private boolean isOccupied;
}
