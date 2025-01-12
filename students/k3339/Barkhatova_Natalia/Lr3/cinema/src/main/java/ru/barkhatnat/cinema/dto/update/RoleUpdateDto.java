package ru.barkhatnat.cinema.dto.update;

import jakarta.validation.constraints.NotNull;
import ru.barkhatnat.cinema.domain.enums.RoleName;

import java.util.UUID;

/**
 * DTO for {@link ru.barkhatnat.cinema.domain.Role}
 */
public record RoleUpdateDto(
        @NotNull(message = "Role name cannot be null")
        RoleName name) {
}