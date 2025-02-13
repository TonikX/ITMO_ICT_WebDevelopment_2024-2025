package org.example.services;

import org.example.entities.Assignment;
import org.example.entities.Submission;
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
public class SubmissionService {

    @PersistenceUnit(unitName = "primary")
    private EntityManagerFactory emf;

    public Submission createSubmission(Assignment assignment, User student, String content) {
        Submission sub = new Submission();
        sub.setAssignment(assignment);
        sub.setStudent(student);
        sub.setContent(content);
        sub.setSubmittedAt(LocalDateTime.now());

        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        try {
            tx.begin();
            em.persist(sub);
            tx.commit();
        } catch (Exception e) {
            if (tx.isActive()) tx.rollback();
            throw e;
        } finally {
            em.close();
        }
        return sub;
    }

    public Submission getById(Long submissionId) {
        EntityManager em = emf.createEntityManager();
        try {
            return em.find(Submission.class, submissionId);
        } finally {
            em.close();
        }
    }

    public Submission setGrade(Submission submission, Integer grade) {
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        try {
            tx.begin();
            Submission managedSub = em.merge(submission);
            managedSub.setGrade(grade);
            tx.commit();
            return managedSub;
        } catch (Exception e) {
            if (tx.isActive()) tx.rollback();
            throw e;
        } finally {
            em.close();
        }
    }

    public List<Submission> getSubmissionsByAssignment(Long assignmentId) {
        EntityManager em = emf.createEntityManager();
        try {
            return em.createQuery(
                            "SELECT s FROM Submission s WHERE s.assignment.assignmentId = :aid",
                            Submission.class
                    )
                    .setParameter("aid", assignmentId)
                    .getResultList();
        } finally {
            em.close();
        }
    }

    public List<Submission> getSubmissionsByStudent(Long studentId) {
        EntityManager em = emf.createEntityManager();
        try {
            return em.createQuery(
                            "SELECT s FROM Submission s WHERE s.student.id = :sid",
                            Submission.class
                    )
                    .setParameter("sid", studentId)
                    .getResultList();
        } finally {
            em.close();
        }
    }
}
