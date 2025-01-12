package ru.barkhatnat.cinema.mapper;

import org.mapstruct.Mapper;
import org.mapstruct.MappingConstants;
import org.mapstruct.MappingTarget;
import org.mapstruct.ReportingPolicy;
import ru.barkhatnat.cinema.domain.Role;
import ru.barkhatnat.cinema.dto.create.RoleCreateDto;
import ru.barkhatnat.cinema.dto.regular.RoleDto;
import ru.barkhatnat.cinema.dto.update.RoleUpdateDto;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE, componentModel = MappingConstants.ComponentModel.SPRING)
public interface RoleMapper {
    Role toEntity(Role role);

    Role toEntity(RoleDto roleDto);

    RoleDto toRoleDto(Role role);

    Role updateWithNull(RoleDto roleDto, @MappingTarget Role role);

    Role toEntity(RoleCreateDto roleCreateDto);

    RoleUpdateDto toRoleUpdateDto(Role role);

    Role updateWithNull(RoleUpdateDto roleUpdateDto, @MappingTarget Role role);
}