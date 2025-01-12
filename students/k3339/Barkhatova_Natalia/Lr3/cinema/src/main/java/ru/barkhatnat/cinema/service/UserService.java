package ru.barkhatnat.cinema.service;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import ru.barkhatnat.cinema.domain.User;
import ru.barkhatnat.cinema.dto.create.UserCreateDto;
import ru.barkhatnat.cinema.dto.regular.UserDto;
import ru.barkhatnat.cinema.dto.update.UserUpdateDto;
import ru.barkhatnat.cinema.mapper.UserMapper;
import ru.barkhatnat.cinema.repository.RoleRepository;
import ru.barkhatnat.cinema.repository.UserRepository;
import ru.barkhatnat.cinema.util.SecurityUtil;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;
    private final RoleRepository roleRepository;
    private final PasswordEncoder passwordEncoder;
    private final SecurityUtil securityUtil;

    public List<UserDto> findAll() {
        List<User> users = userRepository.findAll();
        return users.stream()
                .map(userMapper::toUserDto)
                .toList();
    }

    public UserDto findById(UUID id) {
        User user = userRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "User with id `%s` not found".formatted(id)));
        return userMapper.toUserDto(user);
    }

    public UserDto create(@Valid UserCreateDto userCreateDto) {
        User user = userMapper.toEntity(userCreateDto, roleRepository);
        String encodedPassword = passwordEncoder.encode(user.getPassword());
        User savedUser = userRepository.save(new User(user.getEmail(), encodedPassword,
                user.getFirstName(), user.getLastName(), user.getMiddleName(), user.getRole(), user.getTickets()));
        return userMapper.toUserDto(savedUser);
    }

    public UserUpdateDto update(UUID id, UserUpdateDto userUpdateDto) {
        User user = userRepository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Entity with id `%s` not found".formatted(id)));
        UserUpdateDto updatedUserDto = userUpdateDto;
        if (userUpdateDto.password() != null && !userUpdateDto.password().isEmpty()) {
            String encodedPassword = passwordEncoder.encode(userUpdateDto.password());
            updatedUserDto = new UserUpdateDto(userUpdateDto.email(), encodedPassword, userUpdateDto.firstName(),
                    userUpdateDto.lastName(), userUpdateDto.middleName(), userUpdateDto.roleId());
        }
        userMapper.updateWithNull(updatedUserDto, user, roleRepository);
        User updatedUser = userRepository.save(user);
        return userMapper.toUserUpdateDto(updatedUser);
    }

    public void deleteById(UUID id) {
        userRepository.deleteById(id);
    }

    public UserDto getCurrentUser(){
        UUID currentUserId = securityUtil.getCurrentUserDetails().getUser().getId();
        return findById(currentUserId);
    }
}
