package ru.barkhatnat.cinema.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import ru.barkhatnat.cinema.domain.Row;

import java.util.UUID;

public interface RowRepository extends JpaRepository<Row, UUID> , JpaSpecificationExecutor<Row> {
}