package ru.barkhatnat.homework_board.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.barkhatnat.homework_board.domain.Penalty;

import java.util.UUID;
@Repository
public interface PenaltyRepository extends JpaRepository<Penalty, UUID> {
}