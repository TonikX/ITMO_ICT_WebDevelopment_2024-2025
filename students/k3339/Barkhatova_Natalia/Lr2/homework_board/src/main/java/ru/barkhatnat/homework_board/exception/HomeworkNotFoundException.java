package ru.barkhatnat.homework_board.exception;

import java.util.UUID;

public class HomeworkNotFoundException extends RuntimeException {
    public HomeworkNotFoundException(UUID id) {
        super(String.format("Homework with ID %s not found", id));
    }
}