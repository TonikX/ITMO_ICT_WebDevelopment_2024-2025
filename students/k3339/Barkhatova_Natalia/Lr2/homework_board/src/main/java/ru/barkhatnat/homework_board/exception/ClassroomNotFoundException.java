package ru.barkhatnat.homework_board.exception;

import java.util.UUID;

public class ClassroomNotFoundException extends RuntimeException {
    public ClassroomNotFoundException(UUID id) {
        super(String.format("Classroom with ID %s not found", id));
    }
}
