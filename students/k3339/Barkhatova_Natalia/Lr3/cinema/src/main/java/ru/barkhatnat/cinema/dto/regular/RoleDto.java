package ru.barkhatnat.cinema.dto.regular;

import jakarta.validation.constraints.NotNull;
import ru.barkhatnat.cinema.domain.enums.RoleName;

import java.util.UUID;

/**
 * DTO for {@link ru.barkhatnat.cinema.domain.Role}
 */
public record RoleDto(
        UUID id,
        @NotNull(message = "Role name cannot be null")
        RoleName name) {
}