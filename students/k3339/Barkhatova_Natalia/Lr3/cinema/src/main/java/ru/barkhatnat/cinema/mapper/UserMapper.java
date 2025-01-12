package ru.barkhatnat.cinema.mapper;

import org.mapstruct.*;
import ru.barkhatnat.cinema.domain.Role;
import ru.barkhatnat.cinema.dto.create.UserCreateDto;
import ru.barkhatnat.cinema.domain.User;
import ru.barkhatnat.cinema.dto.regular.UserDto;
import ru.barkhatnat.cinema.dto.update.UserUpdateDto;
import ru.barkhatnat.cinema.repository.RoleRepository;

import java.util.UUID;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE, componentModel = MappingConstants.ComponentModel.SPRING, uses = {RoleMapper.class})
public interface UserMapper {
    UserDto toUserDto(User user);

    @Mapping(target = "role", source = "roleId", qualifiedByName = "mapRole")
    User toEntity(UserCreateDto userCreateDto, @Context RoleRepository roleRepository);

    @Named("mapRole")
    default Role mapRole(UUID roleId, @Context RoleRepository roleRepository) {
        return roleRepository.findById(roleId)
                .orElseThrow(() -> new RuntimeException("Role not found for ID: " + roleId));
    }

    UserCreateDto toUserCreateDto(User user);

    User updateWithNull(UserCreateDto userCreateDto, @MappingTarget User user);

    User updateWithNull(UserDto userDto, @MappingTarget User user);

    UserUpdateDto toUserUpdateDto(User user);

    @Mapping(target = "role", source = "roleId", qualifiedByName = "mapRole")
    User updateWithNull(UserUpdateDto userUpdateDto, @MappingTarget User user, @Context RoleRepository roleRepository);

    User toEntity(UserDto userDto);
}