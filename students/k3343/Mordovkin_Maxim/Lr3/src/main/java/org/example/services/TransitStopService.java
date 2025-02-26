package org.example.services;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;
import org.example.entities.Flight;
import org.example.entities.TransitStop;
import org.jboss.logging.Logger;

import java.util.List;

@ApplicationScoped
public class TransitStopService {

    private static final Logger LOGGER = Logger.getLogger(TransitStopService.class);

    @PersistenceContext(unitName = "AirportPU")
    private EntityManager em;

    @Inject
    private FlightService flightService;

    public List<TransitStop> findAll() {
        return em.createQuery("SELECT ts FROM TransitStop ts", TransitStop.class)
                .getResultList();
    }

    @Transactional
    public TransitStop create(TransitStop transitStop) {
        em.persist(transitStop);
        return transitStop;
    }

    @Transactional
    public TransitStop update(Long id, TransitStop data) {
        TransitStop existing = em.find(TransitStop.class, id);
        if (existing == null) {
            throw new RuntimeException("TransitStop not found");
        }
        existing.setTransitPoint(data.getTransitPoint());
        existing.setTransitArrivalDateTime(data.getTransitArrivalDateTime());
        existing.setTransitDepartureDateTime(data.getTransitDepartureDateTime());
        existing.setFlight(data.getFlight());
        return em.merge(existing);
    }

    @Transactional
    public void delete(Long id) {
        LOGGER.infof("Attempting to delete TransitStop with ID: %d", id);
        TransitStop existing = em.find(TransitStop.class, id);
        if (existing != null) {
            em.remove(existing);
            LOGGER.infof("TransitStop with ID %d removed.", id);
            try {
                em.flush(); // Принудительно синхронизируем изменения с базой данных
                LOGGER.infof("EntityManager flushed after removing TransitStop with ID %d", id);
            } catch (Exception e) {
                LOGGER.errorf("Failed to flush EntityManager after removing TransitStop with ID %d: %s", id, e.getMessage());
                throw new RuntimeException("Failed to remove TransitStop due to flush error: " + e.getMessage());
            }
        } else {
            LOGGER.warnf("TransitStop with ID %d not found.", id);
            throw new RuntimeException("TransitStop not found");
        }
    }

    public TransitStop findById(Long id) {
        return em.find(TransitStop.class, id);
    }

    @Transactional
    public List<TransitStop> findByFlightId(Long flightId) {
        return em.createQuery(
                        "SELECT ts FROM TransitStop ts JOIN FETCH ts.flight WHERE ts.flight.flightId = :fid",
                        TransitStop.class)
                .setParameter("fid", flightId)
                .getResultList();
    }

    @Transactional
    public TransitStop addTransitStop(Long flightId, TransitStop transitStop) {
        Flight flight = flightService.findById(flightId);
        if (flight == null) {
            throw new RuntimeException("Flight not found");
        }
        transitStop.setFlight(flight);
        em.persist(transitStop);
        LOGGER.infof("Added TransitStop with ID: %d to Flight ID: %d", transitStop.getTransitId(), flightId);
        return transitStop;
    }
}

