package ru.barkhatnat.cinema.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.cinema.dto.create.RowCreateDto;
import ru.barkhatnat.cinema.dto.regular.RowDto;
import ru.barkhatnat.cinema.dto.update.RowUpdateDto;
import ru.barkhatnat.cinema.service.RowService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/rest/admin/rows")
@RequiredArgsConstructor
@Tag(name = "Rows", description = "API для управления рядами в зале")
public class RowRestController {

    private final RowService rowService;

    @DeleteMapping
    @Operation(
            summary = "Удалить ряд",
            description = "Удаляет ряд по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "204", description = "Ряд успешно удалён")
            })
    public ResponseEntity<Void> deleteById(@RequestBody UUID id) {
        rowService.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping
    @Operation(
            summary = "Получить все ряды",
            description = "Возвращает список всех рядов",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Ряды успешно получены")
            })
    public ResponseEntity<List<RowDto>> findAll() {
        return ResponseEntity.ok(rowService.findAll());
    }

    @GetMapping("/{id}")
    @Operation(
            summary = "Получить ряд по ID",
            description = "Возвращает ряд по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Ряд успешно получен"),
                    @ApiResponse(responseCode = "404", description = "Ряд не найден")
            })
    public ResponseEntity<RowDto> findById(@PathVariable UUID id) {
        return ResponseEntity.ok(rowService.findById(id));
    }

    @PostMapping
    @Operation(
            summary = "Создать ряд",
            description = "Создает новый ряд на основе переданных данных",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Ряд успешно создан")
            })
    public ResponseEntity<RowDto> create(@RequestBody @Valid RowCreateDto rowCreateDto) {
        return ResponseEntity.ok(rowService.create(rowCreateDto));
    }

    @PutMapping("/{id}")
    @Operation(
            summary = "Обновить ряд",
            description = "Обновляет информацию о ряду по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Ряд успешно обновлен"),
                    @ApiResponse(responseCode = "404", description = "Ряд не найден")
            })
    public ResponseEntity<RowUpdateDto> update(@PathVariable UUID id, @RequestBody RowUpdateDto rowUpdateDto) {
        return ResponseEntity.ok(rowService.update(id, rowUpdateDto));
    }
}
