// src/main/java/org/example/services/CrewMemberService.java
package org.example.services;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;
import jakarta.transaction.Transactional;
import org.example.entities.Crew;
import org.example.entities.CrewMember;
import org.example.entities.Flight;

import java.util.List;

@ApplicationScoped
public class CrewMemberService {

    @PersistenceContext(unitName = "AirportPU")
    private EntityManager em;

    public List<CrewMember> findAll() {
        TypedQuery<CrewMember> query = em.createQuery(
                "SELECT cm FROM CrewMember cm LEFT JOIN FETCH cm.flight LEFT JOIN FETCH cm.user",
                CrewMember.class
        );
        return query.getResultList();
    }

    @Transactional
    public CrewMember create(CrewMember crewMember) {
        System.out.println("Persisting CrewMember: " + crewMember);
        em.persist(crewMember);
        try {
            em.flush(); // Принудительно выполнить INSERT
            System.out.println("Persisted CrewMember: " + crewMember);
        } catch (Exception e) {
            System.out.println("Error persisting CrewMember: " + e.getMessage());
            throw e; // Перебросить исключение для обработки в ресурсном классе
        }
        return crewMember;
    }

    @Transactional
    public CrewMember update(Long id, CrewMember data) {
        CrewMember existing = em.find(CrewMember.class, id);
        if (existing == null) {
            throw new RuntimeException("CrewMember not found");
        }
        existing.setFullName(data.getFullName());
        existing.setAge(data.getAge());
        existing.setEducation(data.getEducation());
        existing.setWorkExperience(data.getWorkExperience());
        existing.setPassportData(data.getPassportData());
        existing.setPermissionType(data.getPermissionType());
        existing.setEmploymentStatus(data.getEmploymentStatus());
        existing.setRoleName(data.getRoleName());
        existing.setFlight(data.getFlight());
        existing.setUser(data.getUser());
        return em.merge(existing);
    }

    @Transactional
    public void delete(Long id) {
        CrewMember existing = em.find(CrewMember.class, id);
        if (existing != null) {
            em.remove(existing);
        }
    }

    public CrewMember findById(Long id) {
        TypedQuery<CrewMember> query = em.createQuery(
                "SELECT cm FROM CrewMember cm LEFT JOIN FETCH cm.flight LEFT JOIN FETCH cm.user WHERE cm.crewMemberId = :id",
                CrewMember.class
        );
        query.setParameter("id", id);
        List<CrewMember> results = query.getResultList();
        return results.isEmpty() ? null : results.get(0);
    }



    @Transactional
    public CrewMember assignToFlight(Long crewMemberId, Long flightId) {
        CrewMember crewMember = em.find(CrewMember.class, crewMemberId);
        Flight flight = em.find(Flight.class, flightId);

        if (crewMember == null) {
            throw new RuntimeException("CrewMember not found, id=" + crewMemberId);
        }
        if (flight == null) {
            throw new RuntimeException("Flight not found, id=" + flightId);
        }

        // 1) Находим (или создаём) объект Crew для данного Flight
        Crew crew = findOrCreateCrewForFlight(flight);

        // 2) Заполняем поля у CrewMember
        crewMember.setFlight(flight); // если вам нужно дублировать flight_id
        crewMember.setCrew(crew);     // чтобы он попал в crewMembers

        // 3) Связываем Crew с CrewMember — чтобы Hibernate видело связь с двух сторон
        crew.getCrewMembers().add(crewMember);

        // 4) Сохраняем
        em.merge(crewMember); // обновить поля CrewMember
        em.merge(crew);       // обновить состав crewMembers

        return crewMember;
    }

    private Crew findOrCreateCrewForFlight(Flight flight) {
        // Ищем, есть ли уже crew для этого рейса
        List<Crew> result = em.createQuery(
                "SELECT c FROM Crew c WHERE c.flight = :f",
                Crew.class
        ).setParameter("f", flight).getResultList();

        if (!result.isEmpty()) {
            // Возвращаем первый (или придумайте логику, если их несколько)
            return result.get(0);
        }

        // Иначе создаём новый:
        Crew newCrew = new Crew();
        newCrew.setFlight(flight);
        em.persist(newCrew);

        return newCrew;
    }

    @Transactional
    public CrewMember removeFromFlight(Long crewMemberId) {
        CrewMember crewMember = em.find(CrewMember.class, crewMemberId);
        if (crewMember != null) {
            crewMember.setFlight(null);
            return em.merge(crewMember);
        }
        throw new RuntimeException("CrewMember not found");
    }
}
