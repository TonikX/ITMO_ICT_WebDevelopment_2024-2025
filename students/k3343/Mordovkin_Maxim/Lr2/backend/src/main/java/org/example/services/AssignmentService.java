package org.example.services;

import org.example.entities.Assignment;
import org.example.entities.User;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.EntityTransaction;
import jakarta.persistence.PersistenceUnit;

import java.time.LocalDateTime;
import java.util.List;

@ApplicationScoped
public class AssignmentService {

    @PersistenceUnit(unitName = "primary")
    private EntityManagerFactory emf;

    public Assignment createAssignment(String title, LocalDateTime dueDate, User teacher) {
        Assignment assignment = new Assignment();
        assignment.setTitle(title);
        assignment.setDueDate(dueDate);
        assignment.setTeacher(teacher);

        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        try {
            tx.begin();
            em.persist(assignment);
            tx.commit();
        } catch (Exception e) {
            if (tx.isActive()) tx.rollback();
            throw e;
        } finally {
            em.close();
        }
        return assignment;
    }

    public List<Assignment> getAllAssignments() {
        EntityManager em = emf.createEntityManager();
        try {
            return em.createQuery("SELECT a FROM Assignment a", Assignment.class)
                    .getResultList();
        } finally {
            em.close();
        }
    }

    public Assignment getAssignmentById(Long id) {
        EntityManager em = emf.createEntityManager();
        try {
            return em.find(Assignment.class, id);
        } finally {
            em.close();
        }
    }

}
