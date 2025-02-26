package org.example.services;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;
import jakarta.transaction.Transactional;
import org.example.entities.CrewMember;
import org.example.entities.Flight;
import org.example.entities.TransitStop;

import java.util.List;

@ApplicationScoped
public class FlightService {

    @PersistenceContext(unitName = "AirportPU")
    private EntityManager em;

    public List<Flight> findAll() {
        TypedQuery<Flight> query = em.createQuery("""
            SELECT distinct f
            FROM Flight f
            LEFT JOIN FETCH f.transitStops
            LEFT JOIN FETCH f.crews c
            LEFT JOIN FETCH c.crewMembers
            """, Flight.class);
        return query.getResultList();
    }

    @Transactional
    public Flight createFlight(Flight flight) {
        if (flight.getAircraft() != null) {
            flight.setTotalSeats(flight.getAircraft().getSeats());
        }
        em.persist(flight);
        return flight;
    }

    @Transactional
    public Flight updateFlight(Long id, Flight data) {
        Flight f = em.find(Flight.class, id);
        if (f == null) {
            throw new RuntimeException("Flight not found");
        }
        // обновляем поля
        f.setDeparturePoint(data.getDeparturePoint());
        f.setDestinationPoint(data.getDestinationPoint());
        f.setDistance(data.getDistance());
        f.setDepartureDateTime(data.getDepartureDateTime());
        f.setArrivalDateTime(data.getArrivalDateTime());
        f.setTicketsSold(data.getTicketsSold());
        if (data.getAircraft() != null) {
            f.setAircraft(data.getAircraft());
            f.setTotalSeats(data.getAircraft().getSeats());
        }
        return em.merge(f);
    }

    @Transactional
    public TransitStop addTransitStop(Long flightId, TransitStop transitStop) {
        Flight flight = em.find(Flight.class, flightId);
        if (flight == null) {
            throw new RuntimeException("Flight not found");
        }
        transitStop.setFlight(flight);
        em.persist(transitStop);
        return transitStop;
    }

    @Transactional
    public void removeTransitStop(Long transitId) {
        TransitStop transitStop = em.find(TransitStop.class, transitId);
        if (transitStop != null) {
            em.remove(transitStop);
        } else {
            throw new RuntimeException("TransitStop not found");
        }
    }

    @Transactional
    public Flight findById(Long id) {
        TypedQuery<Flight> query = em.createQuery("""
            SELECT f
            FROM Flight f
            LEFT JOIN FETCH f.transitStops
            LEFT JOIN FETCH f.crews c
            LEFT JOIN FETCH c.crewMembers
            WHERE f.flightId = :id
            """, Flight.class);
        query.setParameter("id", id);
        List<Flight> result = query.getResultList();
        return result.isEmpty() ? null : result.get(0);
    }

    @Transactional
    public void deleteFlight(Long id) {
        Flight f = em.find(Flight.class, id);
        if (f != null) {
            em.remove(f);
        }
    }
}

