package org.example.services;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;
import org.example.entities.Aircraft;

import java.util.List;

@ApplicationScoped
public class AircraftService {

    @PersistenceContext(unitName = "AirportPU")
    EntityManager em;

    public List<Aircraft> findAll() {
        return em.createQuery("SELECT a FROM Aircraft a", Aircraft.class)
                .getResultList();
    }

    @Transactional
    public Aircraft create(Aircraft a) {
        em.persist(a);
        return a;
    }

    @Transactional
    public Aircraft findById(Long id) {
        return em.find(Aircraft.class, id);
    }


    @Transactional
    public Aircraft update(Long id, Aircraft data) {
        Aircraft existing = em.find(Aircraft.class, id);
        if (existing == null) {
            throw new RuntimeException("Aircraft not found");
        }
        existing.setAircraftType(data.getAircraftType());
        existing.setSeats(data.getSeats());
        existing.setFlightSpeed(data.getFlightSpeed());
        existing.setCarrier(data.getCarrier());
        return em.merge(existing);
    }

    @Transactional
    public void delete(Long id) {
        Aircraft existing = em.find(Aircraft.class, id);
        if (existing != null) {
            em.remove(existing);
        }
    }
}
