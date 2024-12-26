package ru.barkhatnat.homework_board.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import ru.barkhatnat.homework_board.domain.Student;

import java.util.List;
import java.util.UUID;
@Repository
public interface StudentRepository extends JpaRepository<Student, UUID> {
    @Query("SELECT s FROM Student s JOIN s.classrooms c WHERE c.id = :classroomId")
    List<Student> findByClassroomId(@Param("classroomId") UUID classroomId);
}