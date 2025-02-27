package org.example.services;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.PersistenceUnit;
import org.example.dto.ClassStatsDTO;

import java.util.List;

@ApplicationScoped
public class PerformanceService {

    @PersistenceUnit(unitName = "primary")
    private EntityManagerFactory emf;

    /**
     * Возвращает список (assignmentId, title, avgGrade) для заданий,
     * по которым есть хоть одна сдача (Submission) от учеников данного класса.
     */
    public List<ClassStatsDTO> getStatsForClass(Integer classNumber) {
        EntityManager em = emf.createEntityManager();
        try {
            String jpql = """
                SELECT new org.example.dto.ClassStatsDTO(
                        a.assignmentId, a.title, AVG(s.grade)
                    )
                FROM Submission s
                  JOIN s.assignment a
                  JOIN s.student st
                WHERE st.classNumber = :cn
                GROUP BY a.assignmentId, a.title
            """;
            return em.createQuery(jpql, ClassStatsDTO.class)
                    .setParameter("cn", classNumber)
                    .getResultList();
        } finally {
            em.close();
        }
    }
}
