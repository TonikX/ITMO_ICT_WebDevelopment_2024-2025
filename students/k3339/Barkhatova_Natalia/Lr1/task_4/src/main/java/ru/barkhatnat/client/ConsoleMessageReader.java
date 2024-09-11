package ru.barkhatnat.client;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.concurrent.BlockingQueue;
import java.util.function.Consumer;

public class ConsoleMessageReader implements Runnable {

    private static final String COMMAND_QUIT = "/quit";
    private final BlockingQueue<String> outgoingMessagesQueue;
    private final Consumer<Exception> exitHandler;

    public ConsoleMessageReader(final BlockingQueue<String> outgoingMessagesQueue,
                                final Consumer<Exception> exitHandler) {
        this.outgoingMessagesQueue = outgoingMessagesQueue;
        this.exitHandler = exitHandler;
    }

    @Override
    public void run() {
        Exception exception = null;
        try (final BufferedReader reader = new BufferedReader(new InputStreamReader(System.in))) {
            while (!Thread.currentThread().isInterrupted()) {
                if (reader.ready()) {
                    final String message = reader.readLine();
                    if (COMMAND_QUIT.equals(message)) {
                        break;
                    }
                    outgoingMessagesQueue.put(message);
                } else {
                    Thread.sleep(200);
                }
            }
        } catch (final Exception exception1) {
            exception = exception1;
        }
        exitHandler.accept(exception);
    }
}
