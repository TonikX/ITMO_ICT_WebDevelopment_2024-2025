package ru.barkhatnat.cinema.dto.update;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

/**
 * DTO for {@link ru.barkhatnat.cinema.domain.Movie}
 */

public record MovieUpdateDto(
        @Size(message = "Movie name should not exceed 32 characters", max = 32)
        @NotBlank(message = "Movie name cannot be blank")
        String name,

        @NotNull(message = "Duration cannot be null")
        @Min(message = "Duration must be greater than or equal to 1 minute", value = 1)
        @JsonProperty("duration")
        Long duration,

        @Size(message = "Description should not exceed 512 characters", max = 512)
        String description) {
}