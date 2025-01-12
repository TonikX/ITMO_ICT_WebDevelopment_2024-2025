package ru.barkhatnat.cinema.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.cinema.dto.regular.UserDto;
import ru.barkhatnat.cinema.dto.update.UserUpdateDto;
import ru.barkhatnat.cinema.service.UserService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/rest")
@RequiredArgsConstructor
@Tag(name = "Users", description = "API для управления пользователями")
public class UserRestController {

    private final UserService userService;

    @GetMapping("/admin/users")
    @Operation(
            summary = "Получить всех пользователей",
            description = "Возвращает список всех пользователей",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Пользователи успешно получены")
            })
    public ResponseEntity<List<UserDto>> findAll() {
        List<UserDto> userDtos = userService.findAll();
        return ResponseEntity.ok(userDtos);
    }

    @GetMapping("/admin/users/{id}")
    @Operation(
            summary = "Получить пользователя по ID",
            description = "Возвращает пользователя по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Пользователь успешно получен"),
                    @ApiResponse(responseCode = "404", description = "Пользователь не найден")
            })
    public ResponseEntity<UserDto> findById(@PathVariable UUID id) {
        UserDto userDto = userService.findById(id);
        return ResponseEntity.ok(userDto);
    }

    @PutMapping("/users/{id}")
    @Operation(
            summary = "Обновить пользователя",
            description = "Обновляет данные пользователя по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Пользователь успешно обновлен"),
                    @ApiResponse(responseCode = "404", description = "Пользователь не найден")
            })
    public ResponseEntity<UserUpdateDto> update(@PathVariable UUID id, @RequestBody UserUpdateDto userUpdateDto) {
        UserUpdateDto userUpdate = userService.update(id, userUpdateDto);
        return ResponseEntity.ok(userUpdate);
    }

    @DeleteMapping("/admin/users")
    @Operation(
            summary = "Удалить пользователя",
            description = "Удаляет пользователя по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "204", description = "Пользователь успешно удален"),
            })
    public ResponseEntity<Void> deleteById(@RequestBody UUID id) {
        userService.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/me")
    @Operation(
            summary = "Получить текущего пользователя",
            description = "Возвращает текущего пользователя",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Пользователь успешно получен"),
                    @ApiResponse(responseCode = "404", description = "Пользователь не найден")
            })
    public ResponseEntity<UserDto> getCurrentUser() {
        UserDto userDto = userService.getCurrentUser();
        return ResponseEntity.ok(userDto);
    }
}
