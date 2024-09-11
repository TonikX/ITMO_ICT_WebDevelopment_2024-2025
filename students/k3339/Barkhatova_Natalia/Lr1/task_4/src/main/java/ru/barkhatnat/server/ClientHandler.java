package ru.barkhatnat.server;

import ru.barkhatnat.common.*;

import java.io.IOException;
import java.net.Socket;
import java.util.function.BiConsumer;

public class ClientHandler implements Runnable {

    private String userName = null;
    private final Socket socket;

    private final BiConsumer<ClientHandler, Message> messageCallback;
    private final BiConsumer<ClientHandler, Exception> exitCallback;
    public ClientHandler(final Socket socket,
                         final BiConsumer<ClientHandler, Message> messageCallback,
                         final BiConsumer<ClientHandler, Exception> exitCallback) {
        this.socket = socket;
        this.messageCallback = messageCallback;
        this.exitCallback = exitCallback;
    }

    @Override
    public void run() {
        Exception exception = null;
        try (final MessageReader reader = MessageReader.create(socket.getInputStream())) {
            while (!Thread.currentThread().isInterrupted()) {
                final Message message = reader.read();
                if (message instanceof AuthMessage m) {
                    userName = m.username();
                }
                if (userName != null) {
                    messageCallback.accept(this, message);
                }
            }
        } catch (final IOException exception1) {
            exception = exception1;
        }
        exitCallback.accept(this, exception);
    }

    public String getUserName() {
        return userName;
    }

    public void sendMessage(final Message message) throws IOException {
        if (userName == null) {
            return;
        }
        synchronized (socket) {
            MessageWriter.create(socket.getOutputStream()).write(message);
        }
    }
}
