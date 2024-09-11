package ru.barkhatnat.server;

import ru.barkhatnat.common.AuthMessage;

import java.io.IOException;
import java.net.ServerSocket;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.Predicate;

public class Application {

    public static void main(final String[] args) {
        final int port = 1233;
        final Set<ClientHandler> clientHandlers = ConcurrentHashMap.newKeySet();
        try (final ServerSocket socket = new ServerSocket(port)) {
            final ExecutorService pool = Executors.newCachedThreadPool();
            while (true) {
                final ClientHandler clientHandler = new ClientHandler(socket.accept(), (sourceHandler, message) -> {
                    if (message instanceof AuthMessage m) {
                        System.out.printf("Клиент %s подключён\n", m.username());
                    }
                    // выбираю только те хендлеры, которые принадлежат рассматриваемому клиенту.
                    clientHandlers.stream().filter(Predicate.not(sourceHandler::equals)).forEach(handler -> {
                        try {
                            handler.sendMessage(message);
                        } catch (final Exception exception) {
                            System.err.printf("Ошибка отправки сообщения %s: %s\n",
                                    handler.getUserName(),
                                    exception.getMessage());
                        }
                    });
                }, (handler, exception) -> {
                    System.out.printf("Соединение с клиентом %s разорвано\n", handler.getUserName());
                    clientHandlers.remove(handler);
                });
                clientHandlers.add(clientHandler);
                pool.execute(clientHandler);
            }
        } catch (final IOException exception) {
            System.err.printf(
                    "Ошибка запуска сервера на порту %d. Проверьте, не запущел ли уже один экземпляр. Ошибка: %s\n",
                    port,
                    exception.getMessage());
        } catch (final Exception exception) {
            System.err.printf("Неожиданная ошибка запуска сервера на порту %d\n", port);
            exception.printStackTrace(System.err);
        }
    }
}
