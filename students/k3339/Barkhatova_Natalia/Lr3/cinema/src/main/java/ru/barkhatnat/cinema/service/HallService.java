package ru.barkhatnat.cinema.service;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import ru.barkhatnat.cinema.domain.Hall;
import ru.barkhatnat.cinema.dto.create.HallCreateDto;
import ru.barkhatnat.cinema.dto.regular.HallDto;
import ru.barkhatnat.cinema.dto.update.HallUpdateDto;
import ru.barkhatnat.cinema.mapper.HallMapper;
import ru.barkhatnat.cinema.repository.HallRepository;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class HallService {

    private final HallRepository hallRepository;
    private final HallMapper hallMapper;

    public void deleteById(UUID id) {
        hallRepository.deleteById(id);
    }

    public List<HallDto> findAll() {
        List<Hall> halls = hallRepository.findAll();
        return halls.stream()
                .map(hallMapper::toHallDto)
                .toList();
    }

    public HallDto findById(UUID id) {
        Hall hall = hallRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        return hallMapper.toHallDto(hall);
    }

    public HallUpdateDto update(UUID id, HallUpdateDto hallUpdateDto) {
        Hall hall = hallRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        hallMapper.updateWithNull(hallUpdateDto, hall);
        Hall resultHall = hallRepository.save(hall);
        return hallMapper.toHallUpdateDto(resultHall);
    }

    public HallDto save(@Valid HallCreateDto hallCreateDto) {
        Hall hall = hallMapper.toEntity(hallCreateDto);
        Hall resultHall = hallRepository.save(hall);
        return hallMapper.toHallDto(resultHall);
    }
}
