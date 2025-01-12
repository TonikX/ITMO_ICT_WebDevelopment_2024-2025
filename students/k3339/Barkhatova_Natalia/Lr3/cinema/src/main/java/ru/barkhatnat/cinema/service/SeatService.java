package ru.barkhatnat.cinema.service;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import ru.barkhatnat.cinema.domain.Seat;
import ru.barkhatnat.cinema.dto.create.SeatCreateDto;
import ru.barkhatnat.cinema.dto.regular.SeatDto;
import ru.barkhatnat.cinema.dto.update.SeatUpdateDto;
import ru.barkhatnat.cinema.mapper.SeatMapper;
import ru.barkhatnat.cinema.repository.RowRepository;
import ru.barkhatnat.cinema.repository.SeatRepository;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class SeatService {

    private final SeatRepository seatRepository;
    private final SeatMapper seatMapper;
    private final RowRepository rowRepository;

    public void deleteById(UUID id) {
        seatRepository.deleteById(id);
    }

    public List<SeatDto> findAll() {
        List<Seat> seats = seatRepository.findAll();
        return seats.stream()
                .map(seatMapper::toSeatDto)
                .toList();
    }

    public SeatDto findById(UUID id) {
        Seat seat = seatRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        return seatMapper.toSeatDto(seat);
    }

    public SeatDto create(@Valid SeatCreateDto seatCreateDto) {
        Seat seat = seatMapper.toEntity(seatCreateDto, rowRepository);
        Seat savedSeat = seatRepository.save(seat);
        return seatMapper.toSeatDto(savedSeat);
    }

    public SeatUpdateDto update(UUID id, SeatUpdateDto seatUpdateDto) {
        Seat seat = seatRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        seatMapper.updateWithNull(seatUpdateDto, seat, rowRepository);
        Seat updatedSeat = seatRepository.save(seat);
        return seatMapper.toSeatUpdateDto(updatedSeat);
    }
}
