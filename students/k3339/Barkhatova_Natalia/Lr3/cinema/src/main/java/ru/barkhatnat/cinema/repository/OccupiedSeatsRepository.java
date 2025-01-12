package ru.barkhatnat.cinema.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import ru.barkhatnat.cinema.domain.OccupiedSeats;

import java.util.Optional;
import java.util.UUID;

public interface OccupiedSeatsRepository extends JpaRepository<OccupiedSeats, UUID>, JpaSpecificationExecutor<OccupiedSeats> {
    Optional<OccupiedSeats> findBySessionIdAndSeatId(UUID sessionId, UUID seatId);
}