package ru.barkhatnat.client;

import ru.barkhatnat.common.Message;
import ru.barkhatnat.common.MessageReader;

import java.net.Socket;
import java.util.concurrent.BlockingQueue;
import java.util.function.Consumer;

public class ChatMessageReceiver implements Runnable {
    private final BlockingQueue<Message> incomingMessageQueue;
    private final Socket socket;

    private final Consumer<Exception> exitHandler;

    public ChatMessageReceiver(final BlockingQueue<Message> incomingMessageQueue,
                               final Socket socket,
                               final Consumer<Exception> exitHandler) {
        this.incomingMessageQueue = incomingMessageQueue;
        this.socket = socket;
        this.exitHandler = exitHandler;
    }

    @Override
    public void run() {
        Exception exception = null;
        try (final MessageReader reader = MessageReader.create(socket.getInputStream())) {
            while (!Thread.currentThread().isInterrupted()) {
                final Message message = reader.read();
                incomingMessageQueue.put(message);
            }
        } catch (final Exception exception1) {
            exception = exception1;
        }
        exitHandler.accept(exception);
    }
}
