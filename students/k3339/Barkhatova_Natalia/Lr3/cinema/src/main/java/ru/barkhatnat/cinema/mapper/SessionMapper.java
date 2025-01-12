package ru.barkhatnat.cinema.mapper;

import org.mapstruct.*;
import ru.barkhatnat.cinema.domain.Hall;
import ru.barkhatnat.cinema.domain.Movie;
import ru.barkhatnat.cinema.domain.Session;
import ru.barkhatnat.cinema.dto.create.SessionCreateDto;
import ru.barkhatnat.cinema.dto.regular.SessionDto;
import ru.barkhatnat.cinema.dto.update.SessionUpdateDto;
import ru.barkhatnat.cinema.repository.HallRepository;
import ru.barkhatnat.cinema.repository.MovieRepository;

import java.util.UUID;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE, componentModel = MappingConstants.ComponentModel.SPRING, uses = {MovieMapper.class, HallMapper.class})
public interface SessionMapper {
    SessionDto toSessionDto(Session session);

    @Mapping(target = "hall", source = "hallId", qualifiedByName = "mapHall")
    @Mapping(target = "movie", source = "movieId", qualifiedByName = "mapMovie")
    Session toEntity(SessionCreateDto sessionCreateDto, @Context HallRepository hallRepository,
                     @Context MovieRepository movieRepository);

    @Named("mapHall")
    default Hall mapHall(UUID hallId, @Context HallRepository hallRepository) {
        return hallRepository.findById(hallId)
                .orElseThrow(() -> new RuntimeException("Hall not found for ID: " + hallId));
    }

    @Named("mapMovie")
    default Movie mapMovie(UUID movieId, @Context MovieRepository movieRepository) {
        return movieRepository.findById(movieId)
                .orElseThrow(() -> new RuntimeException("Movie not found for ID: " + movieId));
    }

    Session toEntity(SessionDto sessionDto);

    SessionCreateDto toSessionCreateDto(Session session);

    SessionUpdateDto toSessionUpdateDto(Session session);

    @Mapping(target = "hall", source = "hallId", qualifiedByName = "mapHall")
    @Mapping(target = "movie", source = "movieId", qualifiedByName = "mapMovie")
    Session updateWithNull(SessionUpdateDto sessionUpdateDto, @MappingTarget Session session, @Context HallRepository hallRepository,
                           @Context MovieRepository movieRepository
    );
}