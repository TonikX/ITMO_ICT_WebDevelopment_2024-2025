package ru.barkhatnat.homework_board.exception;

import java.util.UUID;

public class SubmissionNotFoundException extends RuntimeException {
    public SubmissionNotFoundException(UUID id) {
        super(String.format("Submission with ID %s not found", id));
    }
}

