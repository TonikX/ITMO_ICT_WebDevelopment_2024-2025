package org.example.entities;

import jakarta.persistence.*;

import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.Getter;



@Getter
@Setter
@NoArgsConstructor
@Entity
@Table(name="aircraft")

//сущность самолёт
public class Aircraft {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long aircraftID;

    @Column(nullable = false)
    private String aircraftType;

    @Column(nullable = false)
    private int seats;

    @Column(nullable = false)
    private double flightSpeed; // или double, если нужно

    @ManyToOne
    @JoinColumn(name = "carrier_id")
    private Carrier carrier;  // связь "многие к одному" с авиаперевозчиком




    public Aircraft(String aircraftType, int seats, double flightSpeed, Carrier carrier) {
        this.aircraftType = aircraftType;
        this.seats = seats;
        this.flightSpeed = flightSpeed;
        this.carrier = carrier;
    }


}
