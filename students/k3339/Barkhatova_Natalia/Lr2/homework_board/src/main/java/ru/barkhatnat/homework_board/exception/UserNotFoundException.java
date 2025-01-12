package ru.barkhatnat.homework_board.exception;

import java.util.UUID;

public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(UUID id) {
        super(String.format("User with ID %s not found", id));
    }
    public UserNotFoundException(String email) {
        super(String.format("User with email %s not found", email));
    }
}
