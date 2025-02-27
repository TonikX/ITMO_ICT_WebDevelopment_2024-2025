package org.example.services;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;

import org.example.entities.AppUser;
import org.example.entities.CrewMember;
import org.example.resources.CrewResource;

import java.util.List;

@ApplicationScoped
public class CrewService {

    @PersistenceContext(unitName = "AirportPU")
    private EntityManager em;

    /**
     * Пользователь подаёт заявку: создаём CrewMember со статусом "PENDING".
     */
    @Transactional
    public void applyForCrew(CrewResource.CrewApplyRequest dto) {
        AppUser user = em.find(AppUser.class, dto.userId);
        if (user == null) {
            throw new RuntimeException("User not found");
        }

        CrewMember cm = new CrewMember();
        cm.setUser(user); // Привязка к AppUser
        cm.setFullName(dto.fullName != null ? dto.fullName : user.getUsername());
        cm.setAge(dto.age);
        cm.setEducation(dto.education);
        cm.setWorkExperience(dto.workExperience);
        cm.setPassportData(dto.passportData);
        cm.setRoleName(dto.role);
        cm.setEmploymentStatus("PENDING");
        cm.setPermissionType("NONE");

        em.persist(cm);
    }

    /**
     * Найти все PENDING
     */
    public List<CrewMember> findPendingCrew() {
        return em.createQuery("""
            SELECT c
            FROM CrewMember c
            WHERE c.employmentStatus = :st
        """, CrewMember.class)
                .setParameter("st", "PENDING")
                .getResultList();
    }

    /**
     * Найти все заявки конкретного юзера
     */
    public List<CrewMember> findByUserId(Long userId) {
        return em.createQuery("""
            SELECT cm
            FROM CrewMember cm
            WHERE cm.user.userId = :uid
        """, CrewMember.class)
                .setParameter("uid", userId)
                .getResultList();
    }

    /**
     * Одобрить заявку
     */
    @Transactional
    public void approveCrew(Long crewMemberId) {
        CrewMember cm = em.find(CrewMember.class, crewMemberId);
        if (cm == null) {
            throw new RuntimeException("CrewMember not found");
        }
        if (!"PENDING".equals(cm.getEmploymentStatus())) {
            throw new RuntimeException("CrewMember is not in PENDING status");
        }
        cm.setEmploymentStatus("WORKING");
        em.merge(cm);
    }

    /**
     * Отклонить заявку
     */
    @Transactional
    public void rejectCrew(Long crewMemberId) {
        CrewMember cm = em.find(CrewMember.class, crewMemberId);
        if (cm == null) {
            throw new RuntimeException("CrewMember not found");
        }
        if (!"PENDING".equals(cm.getEmploymentStatus())) {
            throw new RuntimeException("CrewMember is not in PENDING status");
        }
        cm.setEmploymentStatus("FIRED");
        em.merge(cm);
    }
}
