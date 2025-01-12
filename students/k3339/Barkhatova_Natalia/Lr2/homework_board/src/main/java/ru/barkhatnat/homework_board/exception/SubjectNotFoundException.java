package ru.barkhatnat.homework_board.exception;

import java.util.UUID;

public class SubjectNotFoundException extends RuntimeException {
    public SubjectNotFoundException(UUID id) {
        super(String.format("Subject with ID %s not found", id));
    }
}
