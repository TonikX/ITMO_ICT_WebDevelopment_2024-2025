package ru.barkhatnat.cinema.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.cinema.dto.create.SeatCreateDto;
import ru.barkhatnat.cinema.dto.regular.SeatDto;
import ru.barkhatnat.cinema.dto.update.SeatUpdateDto;
import ru.barkhatnat.cinema.service.SeatService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/rest/admin/seats")
@RequiredArgsConstructor
@Tag(name = "Seats", description = "API для управления местами в зале")
public class SeatRestController {

    private final SeatService seatService;

    @DeleteMapping
    @Operation(
            summary = "Удалить место",
            description = "Удаляет место по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "204", description = "Место успешно удалено")
            })
    public ResponseEntity<Void> deleteById(@RequestBody UUID id) {
        seatService.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping
    @Operation(
            summary = "Получить все места",
            description = "Возвращает список всех мест",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Места успешно получены")
            })
    public ResponseEntity<List<SeatDto>> findAll() {
        return ResponseEntity.ok(seatService.findAll());
    }

    @GetMapping("/{id}")
    @Operation(
            summary = "Получить место по ID",
            description = "Возвращает место по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Место успешно получено"),
                    @ApiResponse(responseCode = "404", description = "Место не найдено")
            })
    public ResponseEntity<SeatDto> findById(@PathVariable UUID id) {
        return ResponseEntity.ok(seatService.findById(id));
    }

    @PostMapping
    @Operation(
            summary = "Создать место",
            description = "Создает новое место на основе переданных данных",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Место успешно создано")
            })
    public ResponseEntity<SeatDto> create(@RequestBody @Valid SeatCreateDto seatCreateDto) {
        return ResponseEntity.ok(seatService.create(seatCreateDto));
    }

    @PutMapping("/{id}")
    @Operation(
            summary = "Обновить место",
            description = "Обновляет информацию о месте по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Место успешно обновлено"),
                    @ApiResponse(responseCode = "404", description = "Место не найдено")
            })
    public ResponseEntity<SeatUpdateDto> update(@PathVariable UUID id, @RequestBody SeatUpdateDto seatUpdateDto) {
        return ResponseEntity.ok(seatService.update(id, seatUpdateDto));
    }
}
