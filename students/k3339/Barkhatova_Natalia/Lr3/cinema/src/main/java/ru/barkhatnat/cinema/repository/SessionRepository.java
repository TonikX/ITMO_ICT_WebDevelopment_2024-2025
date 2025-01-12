package ru.barkhatnat.cinema.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import ru.barkhatnat.cinema.domain.Session;

import java.util.UUID;

public interface SessionRepository extends JpaRepository<Session, UUID>, JpaSpecificationExecutor<Session> {
}