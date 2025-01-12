package ru.barkhatnat.cinema.domain;

import jakarta.persistence.*;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.*;
import org.hibernate.annotations.UuidGenerator;
import ru.barkhatnat.cinema.domain.enums.SeatType;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Seat {
    @Id
    @UuidGenerator
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "row_id", nullable = false)
    @NotNull(message = "Row cannot be null")
    private Row row;

    @Column(nullable = false)
    @Min(value = 1, message = "Seat number must be greater than or equal to 1")
    private Integer number;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    @NotNull(message = "Seat type cannot be null")
    private SeatType type;

    @OneToMany(mappedBy = "seat", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Ticket> tickets = new ArrayList<>();

    @OneToMany(mappedBy = "seat", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OccupiedSeats> occupiedSeats = new ArrayList<>();

    public Seat(Row row, Integer number, SeatType type, List<Ticket> tickets) {
        this.row = row;
        this.number = number;
        this.type = type;
        this.tickets = tickets;
    }
}
