// src/main/java/org/example/entities/Crew.java
package org.example.entities;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.HashSet;
import java.util.Set;

@Getter
@Setter
@NoArgsConstructor
@Entity
@Table(name = "crew")
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
public class Crew {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long crewId;

    // Каждый экипаж привязан к конкретному рейсу (многие к одному уже в Flight)
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "flight_id", nullable = false)
    @JsonBackReference("flight-crews") // Уникальный идентификатор
    private Flight flight;

    // Связь с членами экипажа "один ко многим"
    @OneToMany(mappedBy = "crew", cascade = CascadeType.ALL, orphanRemoval = true)
    @JsonManagedReference("crew-crewMembers") // Уникальный идентификатор
    private Set<CrewMember> crewMembers = new HashSet<>();
}
