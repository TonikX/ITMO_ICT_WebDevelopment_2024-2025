package ru.barkhatnat.cinema.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.barkhatnat.cinema.service.OccupiedSeatsService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.UUID;

@RestController
@RequestMapping("/rest/seats")
@RequiredArgsConstructor
@Tag(name = "Occupied Seats", description = "API для управления занятыми и свободными местами в сеансах")
public class OccupiedSeatsController {

    private final OccupiedSeatsService occupiedSeatsService;
//
//    @GetMapping("/{sessionId}/{seatId}/status")
//    @Operation(
//            summary = "Проверить статус места",
//            description = "Проверяет, занято ли указанное место на сеансе",
//            responses = {
//                    @ApiResponse(responseCode = "200", description = "Статус места успешно получен"),
//            })
//    public ResponseEntity<Boolean> isSeatOccupied(@PathVariable UUID sessionId, @PathVariable UUID seatId) {
//        boolean isOccupied = occupiedSeatsService.isSeatOccupied(sessionId, seatId);
//        return ResponseEntity.ok(isOccupied);
//    }
//
//    @PostMapping("/{sessionId}/{seatId}/occupy")
//    @Operation(
//            summary = "Занять место",
//            description = "Отметить место как занятое на указанном сеансе",
//            responses = {
//                    @ApiResponse(responseCode = "200", description = "Место успешно занято"),
//                    @ApiResponse(responseCode = "404", description = "Сеанс или место не найдено")
//            })
//    public ResponseEntity<Void> occupySeat(@PathVariable UUID sessionId, @PathVariable UUID seatId) {
//        occupiedSeatsService.markSeatAsOccupied(sessionId, seatId);
//        return ResponseEntity.ok().build();
//    }

    @PostMapping("/{sessionId}/{seatId}/free")
    @Operation(
            summary = "Освободить место",
            description = "Отметить место как свободное на указанном сеансе",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Место успешно освобождено"),
                    @ApiResponse(responseCode = "404", description = "Сеанс или место не найдено")
            })
    public ResponseEntity<Void> freeSeat(@PathVariable UUID sessionId, @PathVariable UUID seatId) {
        occupiedSeatsService.markSeatAsFree(sessionId, seatId);
        return ResponseEntity.ok().build();
    }
}
