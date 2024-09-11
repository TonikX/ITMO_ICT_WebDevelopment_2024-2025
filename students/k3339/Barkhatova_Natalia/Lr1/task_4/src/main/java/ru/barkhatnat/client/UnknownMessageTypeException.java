package ru.barkhatnat.client;

import ru.barkhatnat.common.Message;

public class UnknownMessageTypeException extends Exception{
    private final Message receivedMessage;

    public UnknownMessageTypeException(Message receivedMessage) {
        super("Получение сообщений данного типа не поддерживается: " + receivedMessage);
        this.receivedMessage = receivedMessage;
    }

    public Message getReceivedMessage() {
        return receivedMessage;
    }
}