// org.example.config.DataInitializer.java

package org.example.config;

import jakarta.annotation.PostConstruct;
import jakarta.ejb.Singleton;
import jakarta.ejb.Startup;
import jakarta.inject.Inject;
import org.example.entities.Aircraft;
import org.example.entities.Carrier;
import org.example.services.AircraftService;
import org.example.services.CarrierService;

@Singleton
@Startup
public class DataInitializer {

    @Inject
    private AircraftService aircraftService;

    @Inject
    private CarrierService carrierService;

    @PostConstruct
    public void init() {
        if (carrierService.findAll().isEmpty()) {
            Carrier carrierA = new Carrier();
            carrierA.setCarrierName("Airline A");
            Carrier carrierB = new Carrier();
            carrierB.setCarrierName("Airline B");
            carrierService.create(carrierA);
            carrierService.create(carrierB);

            aircraftService.create(new Aircraft("Boeing 737", 160, 850.0, carrierA));
            aircraftService.create(new Aircraft("Airbus A320", 150, 830.0, carrierA));
            aircraftService.create(new Aircraft("Boeing 777", 300, 900.0, carrierB));
            aircraftService.create(new Aircraft("Airbus A380", 500, 920.0, carrierB));
            aircraftService.create(new Aircraft("Embraer E190", 100, 800.0, carrierA));
        }
    }
}
