package ru.barkhatnat.cinema.service;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import ru.barkhatnat.cinema.domain.Movie;
import ru.barkhatnat.cinema.dto.create.MovieCreateDto;
import ru.barkhatnat.cinema.dto.regular.MovieDto;
import ru.barkhatnat.cinema.dto.update.MovieUpdateDto;
import ru.barkhatnat.cinema.mapper.MovieMapper;
import ru.barkhatnat.cinema.repository.MovieRepository;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class MovieService {

    private final MovieRepository movieRepository;
    private final MovieMapper movieMapper;

    public void deleteById(UUID id) {
        movieRepository.deleteById(id);
    }

    public List<MovieDto> findAll() {
        List<Movie> movies = movieRepository.findAll();
        return movies.stream()
                .map(movieMapper::toMovieDto)
                .toList();
    }

    public MovieDto findById(UUID id) {
        Movie movie = movieRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        return movieMapper.toMovieDto(movie);
    }

    public MovieDto create(@Valid MovieCreateDto movieCreateDto) {
        Movie movie = movieMapper.toEntity(movieCreateDto);
        Movie resultMovie = movieRepository.save(movie);
        return movieMapper.toMovieDto(resultMovie);
    }

    public MovieUpdateDto update(UUID id, MovieUpdateDto movieUpdateDto) {
        Movie movie = movieRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        movieMapper.updateWithNull(movieUpdateDto, movie);
        Movie resultMovie = movieRepository.save(movie);
        return movieMapper.toMovieUpdateDto(resultMovie);
    }
}
