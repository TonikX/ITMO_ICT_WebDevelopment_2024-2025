package ru.barkhatnat.cinema.service;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import ru.barkhatnat.cinema.domain.Role;
import ru.barkhatnat.cinema.dto.create.RoleCreateDto;
import ru.barkhatnat.cinema.dto.regular.RoleDto;
import ru.barkhatnat.cinema.dto.update.RoleUpdateDto;
import ru.barkhatnat.cinema.mapper.RoleMapper;
import ru.barkhatnat.cinema.repository.RoleRepository;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class RoleService {

    private final RoleRepository roleRepository;
    private final RoleMapper roleMapper;

    public void deleteById(UUID id) {
        roleRepository.deleteById(id);
    }

    public List<RoleDto> findAll() {
        List<Role> roles = roleRepository.findAll();
        return roles.stream()
                .map(roleMapper::toRoleDto)
                .toList();
    }

    public RoleDto findById(UUID id) {
        Role role = roleRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        return roleMapper.toRoleDto(role);
    }

    public RoleDto create(@Valid RoleCreateDto roleCreateDto) {
        Role role = roleMapper.toEntity(roleCreateDto);
        Role resultRole = roleRepository.save(role);
        return roleMapper.toRoleDto(resultRole);
    }

    public RoleUpdateDto update(UUID id, RoleUpdateDto roleUpdateDto) {
        Role role = roleRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        roleMapper.updateWithNull(roleUpdateDto, role);
        Role resultRole = roleRepository.save(role);
        return roleMapper.toRoleUpdateDto(resultRole);
    }
}