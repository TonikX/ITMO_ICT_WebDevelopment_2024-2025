package ru.barkhatnat.homework_board.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.barkhatnat.homework_board.domain.Teacher;

import java.util.UUID;
@Repository
public interface TeacherRepository extends JpaRepository<Teacher, UUID> {
}