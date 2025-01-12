package ru.barkhatnat.cinema.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.cinema.dto.create.SessionCreateDto;
import ru.barkhatnat.cinema.dto.regular.SessionDto;
import ru.barkhatnat.cinema.dto.update.SessionUpdateDto;
import ru.barkhatnat.cinema.service.SessionService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/rest/admin/sessions")
@RequiredArgsConstructor
@Tag(name = "Sessions", description = "API для управления сеансами")
public class SessionRestController {

    private final SessionService sessionService;

    @DeleteMapping
    @Operation(
            summary = "Удалить сеанс",
            description = "Удаляет сеанс по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "204", description = "Сеанс успешно удален")
            })
    public ResponseEntity<Void> deleteById(@RequestBody UUID id) {
        sessionService.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    @PutMapping("/{id}")
    @Operation(
            summary = "Обновить сеанс",
            description = "Обновляет информацию о сеансе по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Сеанс успешно обновлен"),
                    @ApiResponse(responseCode = "404", description = "Сеанс не найден")
            })
    public ResponseEntity<SessionUpdateDto> update(@PathVariable UUID id, @RequestBody SessionUpdateDto sessionUpdateDto) {
        return ResponseEntity.ok(sessionService.update(id, sessionUpdateDto));
    }

    @GetMapping
    @Operation(
            summary = "Получить все сеансы",
            description = "Возвращает список всех сеансов",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Сеансы успешно получены")
            })
    public ResponseEntity<List<SessionDto>> findAll() {
        return ResponseEntity.ok(sessionService.findAll());
    }

    @GetMapping("/{id}")
    @Operation(
            summary = "Получить сеанс по ID",
            description = "Возвращает сеанс по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Сеанс успешно получен"),
                    @ApiResponse(responseCode = "404", description = "Сеанс не найден")
            })
    public ResponseEntity<SessionDto> findById(@PathVariable UUID id) {
        return ResponseEntity.ok(sessionService.findById(id));
    }

    @PostMapping
    @Operation(
            summary = "Создать сеанс",
            description = "Создает новый сеанс на основе переданных данных",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Сеанс успешно создан")
            })
    public ResponseEntity<SessionDto> create(@RequestBody @Valid SessionCreateDto sessionCreateDto) {
        return ResponseEntity.ok(sessionService.create(sessionCreateDto));
    }
}
