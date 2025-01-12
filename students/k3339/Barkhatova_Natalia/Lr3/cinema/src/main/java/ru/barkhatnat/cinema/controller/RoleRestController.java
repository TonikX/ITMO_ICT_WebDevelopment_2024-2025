package ru.barkhatnat.cinema.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.cinema.dto.create.RoleCreateDto;
import ru.barkhatnat.cinema.dto.regular.RoleDto;
import ru.barkhatnat.cinema.dto.update.RoleUpdateDto;
import ru.barkhatnat.cinema.service.RoleService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/rest/admin/roles")
@RequiredArgsConstructor
@Tag(name = "Roles", description = "API для управления ролями пользователей")
public class RoleRestController {

    private final RoleService roleService;

    @DeleteMapping
    @Operation(
            summary = "Удалить роль",
            description = "Удаляет роль по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "204", description = "Роль успешно удалена"),
            })
    public ResponseEntity<Void> deleteById(@RequestBody UUID id) {
        roleService.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping
    @Operation(
            summary = "Получить все роли",
            description = "Возвращает список всех ролей",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Роли успешно получены")
            })
    public ResponseEntity<List<RoleDto>> findAll() {
        return ResponseEntity.ok(roleService.findAll());
    }

    @GetMapping("/{id}")
    @Operation(
            summary = "Получить роль по ID",
            description = "Возвращает роль по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Роль успешно получена"),
                    @ApiResponse(responseCode = "404", description = "Роль не найдена")
            })
    public ResponseEntity<RoleDto> findById(@PathVariable UUID id) {
        return ResponseEntity.ok(roleService.findById(id));
    }

    @PostMapping
    @Operation(
            summary = "Создать роль",
            description = "Создает новую роль на основе переданных данных",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Роль успешно создана")
            })
    public ResponseEntity<RoleDto> create(@RequestBody @Valid RoleCreateDto roleCreateDto) {
        return ResponseEntity.ok(roleService.create(roleCreateDto));
    }

    @PutMapping("/{id}")
    @Operation(
            summary = "Обновить роль",
            description = "Обновляет информацию о роли по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Роль успешно обновлена"),
                    @ApiResponse(responseCode = "404", description = "Роль не найдена")
            })
    public ResponseEntity<RoleUpdateDto> update(@PathVariable UUID id, @RequestBody RoleUpdateDto roleUpdateDto) {
        return ResponseEntity.ok(roleService.update(id, roleUpdateDto));
    }
}
