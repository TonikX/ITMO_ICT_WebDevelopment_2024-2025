package ru.barkhatnat.cinema.dto.create;

import jakarta.validation.constraints.NotNull;
import ru.barkhatnat.cinema.domain.enums.RoleName;

/**
 * DTO for {@link ru.barkhatnat.cinema.domain.Role}
 */
public record RoleCreateDto(
        @NotNull(message = "Role name cannot be null")
        RoleName name) {
}