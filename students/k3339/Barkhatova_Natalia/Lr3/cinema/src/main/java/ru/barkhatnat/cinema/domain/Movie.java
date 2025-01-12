package ru.barkhatnat.cinema.domain;

import jakarta.persistence.*;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.*;
import org.hibernate.annotations.UuidGenerator;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Movie {
    @Id
    @UuidGenerator
    private UUID id;

    @Column(nullable = false, length = 32)
    @NotBlank(message = "Movie name cannot be blank")
    @Size(max = 32, min = 1, message = "Movie name should not exceed 32 characters")
    private String name;

    @Column(nullable = false)
    @NotNull(message = "Duration cannot be null")
    @Min(message = "Duration must be greater than or equal to 1 minute", value = 1)
    private Long duration;

    @Column(length = 512)
    @Size(max = 512, message = "Description should not exceed 512 characters")
    private String description;

    @OneToMany(mappedBy = "movie", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Session> sessions = new ArrayList<>();

    public Movie(String name, Long duration, String description, List<Session> sessions) {
        this.name = name;
        this.duration = duration;
        this.description = description;
        this.sessions = sessions;
    }
}
