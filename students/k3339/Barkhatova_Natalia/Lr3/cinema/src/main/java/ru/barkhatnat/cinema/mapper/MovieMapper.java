package ru.barkhatnat.cinema.mapper;

import org.mapstruct.*;
import ru.barkhatnat.cinema.dto.create.MovieCreateDto;
import ru.barkhatnat.cinema.domain.Movie;
import ru.barkhatnat.cinema.dto.regular.MovieDto;
import ru.barkhatnat.cinema.dto.update.MovieUpdateDto;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE, componentModel = MappingConstants.ComponentModel.SPRING)
public interface MovieMapper {
    Movie toEntity(MovieDto movieDto);

    MovieDto toMovieDto(Movie movie);

    Movie toEntity(MovieCreateDto movieCreateDto);

    MovieUpdateDto toMovieUpdateDto(Movie movie);

    Movie updateWithNull(MovieUpdateDto movieUpdateDto, @MappingTarget Movie movie);

    Movie updateWithNull(MovieDto movieDto, @MappingTarget Movie movie);
}