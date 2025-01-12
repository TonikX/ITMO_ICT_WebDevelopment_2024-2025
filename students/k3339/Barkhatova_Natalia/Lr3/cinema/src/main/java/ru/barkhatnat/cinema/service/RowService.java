package ru.barkhatnat.cinema.service;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import ru.barkhatnat.cinema.domain.Row;
import ru.barkhatnat.cinema.dto.create.RowCreateDto;
import ru.barkhatnat.cinema.dto.regular.RowDto;
import ru.barkhatnat.cinema.dto.update.RowUpdateDto;
import ru.barkhatnat.cinema.mapper.RowMapper;
import ru.barkhatnat.cinema.repository.HallRepository;
import ru.barkhatnat.cinema.repository.RowRepository;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class RowService {

    private final RowRepository rowRepository;
    private final RowMapper rowMapper;
    private final HallRepository hallRepository;

    public void deleteById(UUID id) {
        rowRepository.deleteById(id);
    }

    public List<RowDto> findAll() {
        List<Row> rows = rowRepository.findAll();
        return rows.stream()
                .map(rowMapper::toRowDto)
                .toList();
    }

    public RowDto findById(UUID id) {
        Row row = rowRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        return rowMapper.toRowDto(row);
    }

    public RowDto create(@Valid RowCreateDto rowCreateDto) {
        Row row = rowMapper.toEntity(rowCreateDto, hallRepository);
        Row resultRow = rowRepository.save(row);
        return rowMapper.toRowDto(resultRow);
    }

    public RowUpdateDto update(UUID id, RowUpdateDto rowUpdateDto) {
        Row row = rowRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        rowMapper.updateWithNull(rowUpdateDto, row, hallRepository);
        Row resultRow = rowRepository.save(row);
        return rowMapper.toRowUpdateDto(resultRow);
    }
}