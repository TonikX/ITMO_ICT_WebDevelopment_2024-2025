package ru.barkhatnat.common;

public record ChatMessage(String username, String message) implements Message{
}
