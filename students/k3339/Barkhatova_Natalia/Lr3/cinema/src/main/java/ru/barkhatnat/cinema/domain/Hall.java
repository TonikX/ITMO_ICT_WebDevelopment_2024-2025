package ru.barkhatnat.cinema.domain;

import jakarta.persistence.*;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.*;
import lombok.experimental.FieldNameConstants;
import org.hibernate.annotations.UuidGenerator;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Getter
@Setter
@FieldNameConstants
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Hall {
    @Id
    @UuidGenerator
    private UUID id;

    @Column(nullable = false, length = 32)
    @NotBlank(message = "Hall name cannot be blank")
    @Size(max = 32, min = 1, message = "Hall name should not exceed 32 characters")
    private String name;

    @Column(nullable = false, columnDefinition = "integer default 0")
    @Min(value = 0, message = "Capacity cannot be negative")
    private Integer capacity;

    @OneToMany(mappedBy = "hall", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Row> rows = new ArrayList<>();

    @OneToMany(mappedBy = "hall", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Session> sessions = new ArrayList<>();

    public Hall(String name, Integer capacity, List<Row> rows, List<Session> sessions) {
        this.name = name;
        this.capacity = capacity;
        this.rows = rows;
        this.sessions = sessions;
    }
}
