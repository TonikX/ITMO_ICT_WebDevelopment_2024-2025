package ru.barkhatnat.client;

import ru.barkhatnat.common.AuthMessage;
import ru.barkhatnat.common.ChatMessage;
import ru.barkhatnat.common.Message;

import java.util.Map;
import java.util.concurrent.BlockingQueue;
import java.util.function.Consumer;
import java.util.function.Function;

public class ConsoleMessageWriter implements Runnable {

    private static final Map<Class<? extends Message>, Function<? extends Message, String>> MESSAGE_CREATORS =
            Map.<Class<? extends Message>, Function<? extends Message, String>>of(AuthMessage.class,
                    (final AuthMessage message) -> String.format("Подключился пользователь: %s",
                            message.username()),
                    ChatMessage.class,
                    (final ChatMessage message) -> String.format("[%s] %s",
                            message.username(),
                            message.message()));

    private final BlockingQueue<Message> incomingMessageQueue;

    private final Consumer<Exception> errorHandler;

    public ConsoleMessageWriter(final BlockingQueue<Message> incomingMessageQueue,
                                final Consumer<Exception> errorHandler) {
        this.incomingMessageQueue = incomingMessageQueue;
        this.errorHandler = errorHandler;
    }

    @Override
    public void run() {
        while (!Thread.currentThread().isInterrupted()) {
            try {
                final Message message = incomingMessageQueue.take();
                @SuppressWarnings("unchecked") final Function<Message, String> creator =
                        (Function<Message, String>) MESSAGE_CREATORS.get(message.getClass());
                if (creator == null) {
                    throw new UnknownMessageTypeException(message);
                }
                System.out.println(creator.apply(message));
            } catch (final Exception exception) {
                errorHandler.accept(exception);
            }
        }
    }
}
