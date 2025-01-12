package ru.barkhatnat.cinema.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.cinema.dto.create.HallCreateDto;
import ru.barkhatnat.cinema.dto.regular.HallDto;
import ru.barkhatnat.cinema.dto.update.HallUpdateDto;
import ru.barkhatnat.cinema.service.HallService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/rest/admin/halls")
@RequiredArgsConstructor
@Tag(name = "Hall Management", description = "API для управления залами кинотеатра")
public class HallRestController {

    private final HallService hallService;

    @DeleteMapping
    @Operation(
            summary = "Удалить зал по идентификатору",
            description = "Удаляет зал кинотеатра по уникальному идентификатору.",
            responses = {
                    @ApiResponse(responseCode = "204", description = "Зал успешно удален"),
            })
    public ResponseEntity<Void> deleteById(@RequestBody @Parameter(description = "UUID идентификатор зала") UUID id) {
        hallService.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping
    @Operation(
            summary = "Получить список всех залов",
            description = "Возвращает список всех залов в кинотеатре.",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Список залов получен")
            })
    public ResponseEntity<List<HallDto>> findAll() {
        List<HallDto> halls = hallService.findAll();
        if (halls.isEmpty()) {
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.ok(halls);
    }

    @GetMapping("/{id}")
    @Operation(
            summary = "Получить зал по идентификатору",
            description = "Возвращает зал по его уникальному идентификатору.",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Зал найден"),
                    @ApiResponse(responseCode = "404", description = "Зал не найден")
            })
    public ResponseEntity<HallDto> findById(@PathVariable UUID id) {
        HallDto hallDto = hallService.findById(id);
        return ResponseEntity.ok(hallDto);
    }

    @PutMapping("/{id}")
    @Operation(
            summary = "Обновить данные зала",
            description = "Обновляет информацию о зале по уникальному идентификатору.",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Зал успешно обновлен"),
                    @ApiResponse(responseCode = "404", description = "Зал не найден"),
            })
    public ResponseEntity<HallUpdateDto> update(
            @PathVariable UUID id,
            @RequestBody @Parameter(description = "Обновленные данные зала") HallUpdateDto hallUpdateDto) {
        HallUpdateDto updatedHall = hallService.update(id, hallUpdateDto);
        return ResponseEntity.ok(updatedHall);
    }

    @PostMapping
    @Operation(
            summary = "Создать новый зал",
            description = "Создает новый зал в кинотеатре.",
            responses = {
                    @ApiResponse(responseCode = "201", description = "Зал успешно создан"),
            })
    public ResponseEntity<HallDto> save(
            @RequestBody @Valid @Parameter(description = "Данные для создания нового зала") HallCreateDto hallCreateDto) {
        HallDto createdHall = hallService.save(hallCreateDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdHall);
    }
}
