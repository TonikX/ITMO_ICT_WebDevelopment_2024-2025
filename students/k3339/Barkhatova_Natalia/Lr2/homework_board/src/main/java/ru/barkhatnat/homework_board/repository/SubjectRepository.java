package ru.barkhatnat.homework_board.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.barkhatnat.homework_board.domain.Subject;

import java.util.List;
import java.util.UUID;
@Repository
public interface SubjectRepository extends JpaRepository<Subject, UUID> {
    List<Subject> findByTeacherEmail(String email);
}