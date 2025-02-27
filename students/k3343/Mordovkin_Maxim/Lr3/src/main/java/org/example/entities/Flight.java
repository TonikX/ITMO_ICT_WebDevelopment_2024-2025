
package org.example.entities;

import com.fasterxml.jackson.annotation.JsonManagedReference;
import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Getter
@Setter
@NoArgsConstructor

@Entity
@Table(name = "flight")
public class Flight {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long flightId;

    @Column(nullable = false)
    private String departurePoint;

    @Column(nullable = false)
    private String destinationPoint;

    @Column(nullable = false)
    private double distance;

    @Column(nullable = false)
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime departureDateTime;

    @Column(nullable = false)
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime arrivalDateTime;

    @Column(nullable = false)
    private int ticketsSold;

    @Column(nullable = false)
    private int totalSeats;

    // Связь с самолетом (многие к одному)
    @ManyToOne
    @JoinColumn(name = "aircraft_id")
    private Aircraft aircraft;

    // Связь с транзитными посадками (один ко многим)
    @OneToMany(mappedBy = "flight", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.EAGER)
    @JsonManagedReference
    private List<TransitStop> transitStops;

    // Связь с экипажем (один ко многим)
    @OneToMany(mappedBy = "flight", fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    private Set<Crew> crews = new HashSet<>();
}

