package ru.barkhatnat.cinema.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import ru.barkhatnat.cinema.domain.Seat;

import java.util.UUID;

public interface SeatRepository extends JpaRepository<Seat, UUID>, JpaSpecificationExecutor<Seat> {
}