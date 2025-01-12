package ru.barkhatnat.cinema.domain;

import jakarta.persistence.*;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.*;
import org.hibernate.annotations.UuidGenerator;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Entity
@Getter
@Setter
@NoArgsConstructor
@Builder
@AllArgsConstructor
public class Session {
    @Id
    @UuidGenerator
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "movie_id", nullable = false)
    @NotNull(message = "Movie cannot be null")
    private Movie movie;

    @ManyToOne
    @JoinColumn(name = "hall_id", nullable = false)
    @NotNull(message = "Hall cannot be null")
    private Hall hall;

    @Column(name = "start_time", nullable = false, columnDefinition = "TIMESTAMP")
    @NotNull(message = "Start time cannot be null")
    private LocalDateTime startTime;

    @Column(nullable = false)
    @Min(value = 1, message = "Price must be greater than or equal to 0")
    private Integer price;

    @OneToMany(mappedBy = "session", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OccupiedSeats> occupiedSeats;
}