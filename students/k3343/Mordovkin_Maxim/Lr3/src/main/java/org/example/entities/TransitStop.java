package org.example.entities;

import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor

@Entity
@Table(name = "transit_stop")
public class TransitStop {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "transitid") // Сопоставление с первичным ключом 'transitid'
    private Long transitId;

    // Если 'transitstop_id' необходим как дополнительное поле
    @Column(name = "transitstop_id", nullable = false, insertable = false, updatable = false)
    private Long transitStopId;

    @Column(nullable = false)
    private String transitPoint;

    @Column(nullable = false)
    private LocalDateTime transitArrivalDateTime;

    @Column(nullable = false)
    private LocalDateTime transitDepartureDateTime;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "flight_id", nullable = false)
    @JsonBackReference
    private Flight flight;
}

