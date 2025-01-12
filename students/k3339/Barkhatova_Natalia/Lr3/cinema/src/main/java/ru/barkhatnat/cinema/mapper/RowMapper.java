package ru.barkhatnat.cinema.mapper;

import org.mapstruct.*;
import ru.barkhatnat.cinema.domain.Hall;
import ru.barkhatnat.cinema.dto.create.RowCreateDto;
import ru.barkhatnat.cinema.dto.regular.RowDto;
import ru.barkhatnat.cinema.domain.Row;
import ru.barkhatnat.cinema.dto.update.RowUpdateDto;
import ru.barkhatnat.cinema.repository.HallRepository;

import java.util.UUID;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE, componentModel = MappingConstants.ComponentModel.SPRING, uses = {HallMapper.class})
public interface RowMapper {
    RowDto toRowDto(Row row);

    @Mapping(target = "hall", source = "hallId", qualifiedByName = "mapHall")
    Row toEntity(RowCreateDto rowCreateDto, @Context HallRepository hallRepository);

    @Named("mapHall")
    default Hall mapHall(UUID hallId, @Context HallRepository hallRepository) {
        return hallRepository.findById(hallId)
                .orElseThrow(() -> new RuntimeException("Hall not found for ID: " + hallId));
    }
    Row toEntity(RowDto rowDto);

    RowCreateDto toRowCreateDto(Row row);

    RowUpdateDto toRowUpdateDto(Row row);

    @Mapping(target = "hall", source = "hallId", qualifiedByName = "mapHall")
    Row updateWithNull(RowUpdateDto rowUpdateDto, @MappingTarget Row row, @Context HallRepository hallRepository);
}