package ru.barkhatnat.cinema.dto.create;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/**
 * DTO for {@link ru.barkhatnat.cinema.domain.Hall}
 */
public record HallCreateDto(
        @Size(message = "Hall name should not exceed 32 characters", max = 32)
        @NotBlank(message = "Hall name cannot be blank")
        String name,

        @Min(message = "Capacity cannot be negative", value = 0)
        Integer capacity) {
}