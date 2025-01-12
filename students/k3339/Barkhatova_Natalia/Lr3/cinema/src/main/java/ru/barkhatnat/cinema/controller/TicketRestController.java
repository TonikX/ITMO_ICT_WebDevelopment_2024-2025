package ru.barkhatnat.cinema.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.cinema.dto.create.TicketCreateDto;
import ru.barkhatnat.cinema.dto.regular.TicketDto;
import ru.barkhatnat.cinema.dto.update.TicketUpdateDto;
import ru.barkhatnat.cinema.service.TicketService;
import ru.barkhatnat.cinema.util.SecurityUtil;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/rest")
@RequiredArgsConstructor
@Tag(name = "Tickets", description = "API для управления билетами")
public class TicketRestController {

    private final TicketService ticketService;
    private final SecurityUtil securityUtil;

    @DeleteMapping("/admin/tickets")
    @Operation(
            summary = "Удалить билет",
            description = "Удаляет билет по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "204", description = "Билет успешно удален"),
            })
    public ResponseEntity<Void> deleteById(@RequestBody UUID id) {
        ticketService.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    @PutMapping("/admin/tickets/{id}")
    @Operation(
            summary = "Обновить билет",
            description = "Обновляет информацию о билете по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Билет успешно обновлен"),
                    @ApiResponse(responseCode = "404", description = "Билет не найден")
            })
    public ResponseEntity<TicketUpdateDto> update(@PathVariable UUID id, @RequestBody TicketUpdateDto ticketUpdateDto) {
        return ResponseEntity.ok(ticketService.update(id, ticketUpdateDto));
    }

    @GetMapping("/admin/tickets")
    @Operation(
            summary = "Получить все билеты",
            description = "Возвращает список всех билетов",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Билеты успешно получены")
            })
    public ResponseEntity<List<TicketDto>> findAll() {
        return ResponseEntity.ok(ticketService.findAll());
    }

    @GetMapping("/tickets/user")
    @Operation(
            summary = "Получить билеты текущего пользователя",
            description = "Возвращает все билеты, приобретенные текущим пользователем",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Билеты пользователя успешно получены")
            })
    public ResponseEntity<List<TicketDto>> findAllCurrentUserTickets() {
        UUID currentUserId = securityUtil.getCurrentUserDetails().getUser().getId();
        return ResponseEntity.ok(ticketService.findAll(currentUserId));
    }

    @GetMapping("/tickets/{id}")
    @Operation(
            summary = "Получить билет по ID",
            description = "Возвращает билет по идентификатору",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Билет успешно получен"),
                    @ApiResponse(responseCode = "404", description = "Билет не найден")
            })
    public ResponseEntity<TicketDto> findById(@PathVariable UUID id) {
        UUID currentUserId = securityUtil.getCurrentUserDetails().getUser().getId();
        return ResponseEntity.ok(ticketService.findById(id, currentUserId));
    }

    @PostMapping("/tickets")
    @Operation(
            summary = "Забронировать билет",
            description = "Создает новый билет на основе предоставленных данных",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Билет успешно забронирован"),
                    @ApiResponse(responseCode = "400", description = "Ошибка при бронировании билета")
            })
    public ResponseEntity<TicketDto> create(@RequestBody @Valid TicketCreateDto ticketCreateDto) {
        return ResponseEntity.ok(ticketService.book(ticketCreateDto));
    }
}
