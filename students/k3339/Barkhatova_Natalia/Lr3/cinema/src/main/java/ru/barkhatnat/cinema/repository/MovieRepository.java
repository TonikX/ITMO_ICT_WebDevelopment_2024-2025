package ru.barkhatnat.cinema.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import ru.barkhatnat.cinema.domain.Movie;

import java.util.UUID;

public interface MovieRepository extends JpaRepository<Movie, UUID>, JpaSpecificationExecutor<Movie> {
}