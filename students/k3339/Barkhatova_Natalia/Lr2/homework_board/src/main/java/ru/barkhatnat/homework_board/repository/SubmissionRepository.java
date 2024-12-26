package ru.barkhatnat.homework_board.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import ru.barkhatnat.homework_board.domain.Submission;

import java.util.List;
import java.util.UUID;

@Repository
public interface SubmissionRepository extends JpaRepository<Submission, UUID> {
    @Query("SELECT s FROM Submission s JOIN s.homework h WHERE h.id = :homeworkId")
    List<Submission> findByHomeworkId(@Param("homeworkId") UUID homeworkId);

    @Query("SELECT s FROM Submission s JOIN s.student st JOIN s.homework h WHERE st.id = :studentId and h.id = :homeworkId")
    List<Submission> findByHomeworkIdAndStudentId(@Param("homeworkId") UUID homeworkId, @Param("studentId") UUID studentId);

    @Query("SELECT s FROM Submission s JOIN s.student st JOIN st.classrooms c WHERE c.id = :classroomId")
    List<Submission> findByClassroomId(@Param("classroomId") UUID classroomId);
}