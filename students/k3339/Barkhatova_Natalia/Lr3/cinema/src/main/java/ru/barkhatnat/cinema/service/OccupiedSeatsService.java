package ru.barkhatnat.cinema.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import ru.barkhatnat.cinema.domain.OccupiedSeats;
import ru.barkhatnat.cinema.repository.OccupiedSeatsRepository;

import java.util.UUID;

@Service
@RequiredArgsConstructor
public class OccupiedSeatsService {

    private final OccupiedSeatsRepository occupiedSeatsRepository;

    public boolean isSeatOccupied(UUID sessionId, UUID seatId) {
        return occupiedSeatsRepository.findBySessionIdAndSeatId(sessionId, seatId)
                .map(OccupiedSeats::isOccupied)
                .orElse(false);
    }

    public OccupiedSeats markSeatAsOccupied(UUID sessionId, UUID seatId) {
        return occupiedSeatsRepository.findBySessionIdAndSeatId(sessionId, seatId)
                .map(occupiedSeat -> {
                    occupiedSeat.setOccupied(true);
                    return occupiedSeatsRepository.save(occupiedSeat);
                })
                .orElseThrow(() -> new IllegalArgumentException("Seat or Session not found"));
    }

    public OccupiedSeats markSeatAsFree(UUID sessionId, UUID seatId) {
        return occupiedSeatsRepository.findBySessionIdAndSeatId(sessionId, seatId)
                .map(occupiedSeat -> {
                    occupiedSeat.setOccupied(false);
                    return occupiedSeatsRepository.save(occupiedSeat);
                })
                .orElseThrow(() -> new IllegalArgumentException("Seat or Session not found"));
    }
}
