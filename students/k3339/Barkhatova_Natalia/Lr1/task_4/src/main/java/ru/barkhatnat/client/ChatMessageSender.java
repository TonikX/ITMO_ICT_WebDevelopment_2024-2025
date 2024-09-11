package ru.barkhatnat.client;

import ru.barkhatnat.common.AuthMessage;
import ru.barkhatnat.common.ChatMessage;
import ru.barkhatnat.common.MessageWriter;

import java.net.Socket;
import java.util.concurrent.BlockingQueue;
import java.util.function.Consumer;

public class ChatMessageSender implements Runnable {

    private final BlockingQueue<String> outgoingMessagesQueue;
    private final String userName;
    private final Socket socket;
    private final Consumer<Exception> exitHandler;

    public ChatMessageSender(final BlockingQueue<String> outgoingMessagesQueue,
                             final String userName,
                             final Socket socket,
                             final Consumer<Exception> exitHandler) {
        this.outgoingMessagesQueue = outgoingMessagesQueue;
        this.userName = userName;
        this.socket = socket;
        this.exitHandler = exitHandler;
    }

    @Override
    public void run() {
        try (final MessageWriter writer = MessageWriter.create(socket.getOutputStream())) {
            writer.write(new AuthMessage(userName));
            while (!Thread.currentThread().isInterrupted()) {
                final String message = outgoingMessagesQueue.take();
                writer.write(new ChatMessage(userName, message));
            }
        } catch (final Exception exception) {
            exitHandler.accept(exception);
        }
    }
}