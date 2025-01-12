package ru.barkhatnat.cinema.domain;

import jakarta.persistence.*;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.*;
import org.hibernate.annotations.UuidGenerator;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Row {
    @Id
    @UuidGenerator
    private UUID id;

    @Column(nullable = false)
    @Min(value = 1, message = "Row number must be greater than or equal to 1")
    private Integer number;

    @ManyToOne
    @JoinColumn(name = "hall_id", nullable = false)
    @NotNull(message = "Hall cannot be null")
    private Hall hall;

    @OneToMany(mappedBy = "row", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Seat> seats = new ArrayList<>();

    public Row(Integer number, Hall hall, List<Seat> seats) {
        this.number = number;
        this.hall = hall;
        this.seats = seats;
    }
}
