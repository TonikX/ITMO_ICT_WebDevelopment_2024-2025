package org.example.services;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;
import org.example.entities.AircraftMaintenance;

import java.util.List;

@ApplicationScoped
public class AircraftMaintenanceService {

    @PersistenceContext(unitName = "AirportPU")
    private EntityManager em;

    public List<AircraftMaintenance> findAll() {
        return em.createQuery("SELECT am FROM AircraftMaintenance am", AircraftMaintenance.class)
                .getResultList();
    }

    @Transactional
    public AircraftMaintenance create(AircraftMaintenance maintenance) {
        em.persist(maintenance);
        return maintenance;
    }

    @Transactional
    public AircraftMaintenance update(Long id, AircraftMaintenance data) {
        AircraftMaintenance existing = em.find(AircraftMaintenance.class, id);
        if (existing == null) {
            throw new RuntimeException("AircraftMaintenance not found");
        }
        existing.setMaintenanceStatus(data.getMaintenanceStatus());
        existing.setStartDate(data.getStartDate());
        existing.setEndDate(data.getEndDate());
        existing.setAircraft(data.getAircraft());
        return em.merge(existing);
    }

    @Transactional
    public void delete(Long id) {
        AircraftMaintenance existing = em.find(AircraftMaintenance.class, id);
        if (existing != null) {
            em.remove(existing);
        }
    }

    public AircraftMaintenance findById(Long id) {
        return em.find(AircraftMaintenance.class, id);
    }

    public List<AircraftMaintenance> findByAircraftId(Long aircraftId) {
        return em.createQuery("SELECT am FROM AircraftMaintenance am WHERE am.aircraft.aircraftID = :aid", AircraftMaintenance.class)
                .setParameter("aid", aircraftId)
                .getResultList();
    }
}
