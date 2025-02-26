package org.example.services;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;
import org.example.entities.Carrier;

import java.util.List;

@ApplicationScoped
public class CarrierService {

    @PersistenceContext(unitName = "AirportPU")
    private EntityManager em;

    public List<Carrier> findAll() {
        return em.createQuery("SELECT c FROM Carrier c", Carrier.class)
                .getResultList();
    }

    @Transactional
    public Carrier create(Carrier carrier) {
        em.persist(carrier);
        return carrier;
    }

    @Transactional
    public Carrier update(Long id, Carrier data) {
        Carrier existing = em.find(Carrier.class, id);
        if (existing == null) {
            throw new RuntimeException("Carrier not found");
        }
        existing.setCarrierName(data.getCarrierName());
        return em.merge(existing);
    }

    @Transactional
    public void delete(Long id) {
        Carrier existing = em.find(Carrier.class, id);
        if (existing != null) {
            em.remove(existing);
        }
    }

    public Carrier findById(Long id) {
        return em.find(Carrier.class, id);
    }
}
