package ru.barkhatnat.cinema.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.cinema.dto.create.MovieCreateDto;
import ru.barkhatnat.cinema.dto.regular.MovieDto;
import ru.barkhatnat.cinema.dto.update.MovieUpdateDto;
import ru.barkhatnat.cinema.service.MovieService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/rest/admin/movies")
@RequiredArgsConstructor
@Tag(name = "Movies", description = "API для управления фильмами")
public class MovieRestController {

    private final MovieService movieService;

    @DeleteMapping
    @Operation(
            summary = "Удаление фильма",
            description = "Удаляет фильм по предоставленному ID",
            responses = {
                    @ApiResponse(responseCode = "204", description = "Фильм успешно удален"),
            })
    public ResponseEntity<Void> deleteById(@RequestBody UUID id) {
        movieService.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping
    @Operation(
            summary = "Получить все фильмы",
            description = "Возвращает список всех фильмов",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Список фильмов успешно возвращен")
            })
    public ResponseEntity<List<MovieDto>> findAll() {
        return ResponseEntity.ok(movieService.findAll());
    }

    @GetMapping("/{id}")
    @Operation(
            summary = "Получить фильм по ID",
            description = "Возвращает фильм по предоставленному ID",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Фильм найден и возвращен"),
                    @ApiResponse(responseCode = "404", description = "Фильм с указанным ID не найден")
            })
    public ResponseEntity<MovieDto> findById(@PathVariable UUID id) {
        return ResponseEntity.ok(movieService.findById(id));
    }

    @PostMapping
    @Operation(
            summary = "Создать новый фильм",
            description = "Создает новый фильм на основе предоставленных данных",
            responses = {
                    @ApiResponse(responseCode = "201", description = "Фильм успешно создан")
            })
    public ResponseEntity<MovieDto> create(@RequestBody @Valid MovieCreateDto movieCreateDto) {
        MovieDto movieDto = movieService.create(movieCreateDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(movieDto);
    }

    @PutMapping("/{id}")
    @Operation(
            summary = "Обновить фильм",
            description = "Обновляет информацию о фильме по предоставленному ID",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Фильм успешно обновлен"),
                    @ApiResponse(responseCode = "404", description = "Фильм с указанным ID не найден")
            })
    public ResponseEntity<MovieUpdateDto> update(@PathVariable UUID id, @RequestBody MovieUpdateDto movieUpdateDto) {
        MovieUpdateDto updatedMovie = movieService.update(id, movieUpdateDto);
        return ResponseEntity.ok(updatedMovie);
    }
}
