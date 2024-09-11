package ru.barkhatnat.client;

import ru.barkhatnat.common.Message;

import java.io.IOException;
import java.net.Socket;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.Scanner;
import java.util.concurrent.*;

import static java.util.Arrays.asList;

public class Application {
    public static void main(final String[] args) {
        final BlockingQueue<String> outgoingMessagesQueue = new LinkedBlockingDeque<>(10);
        final BlockingQueue<Message> incomingMessageQueue = new LinkedBlockingDeque<>(50);
        final String address = args.length > 0 ? args[0] : "localhost";
        final int port = args.length > 1 ? Integer.parseInt(args[1]) : 1234;
        try (final Socket socket = new Socket(address, port); final Scanner scanner = new Scanner(System.in)) {
            final String userName = obtainUserName(scanner);
            final ExecutorService pool = Executors.newFixedThreadPool(4);
            final Callable<Object> consoleMessageReaderCallable =
                    Executors.callable(new ConsoleMessageReader(outgoingMessagesQueue, exception -> {
                        if (Thread.currentThread().isInterrupted()) {
                            return;
                        }
                        if (exception != null && !(exception instanceof InterruptedException)) {
                            System.err.println("Ошибка получения сообщения");
                            exception.printStackTrace(System.err);
                        }
                        pool.shutdownNow();
                    }));
            final Callable<Object> chatMessageSenderCallable =
                    Executors.callable(new ChatMessageSender(outgoingMessagesQueue, userName, socket, exception -> {
                        if (Thread.currentThread().isInterrupted()) {
                            return;
                        }
                        if (exception != null && !(exception instanceof InterruptedException)) {
                            System.err.println("Ошибка отправки сообщений на сервер");
                            exception.printStackTrace(System.err);
                        }
                        pool.shutdownNow();
                    }));
            final Callable<Object> consoleMessageWriterCallable =
                    Executors.callable(new ConsoleMessageWriter(incomingMessageQueue, exception -> {
                        if (Thread.currentThread().isInterrupted()) {
                            return;
                        }
                        if (!(exception instanceof InterruptedException)) {
                            System.err.println(exception.getMessage());
                        }
                    }));
            final Callable<Object> chatMessageReceiver =
                    Executors.callable(new ChatMessageReceiver(incomingMessageQueue, socket, exception -> {
                        if (Thread.currentThread().isInterrupted()) {
                            return;
                        }
                        if (exception != null) {
                            if (exception instanceof SocketException) {
                                System.err.println("Сервер порвал соединение");
                            } else if (!(exception instanceof InterruptedException)) {
                                System.err.println("Ошибка обработки данных, полученных от сервера");
                                exception.printStackTrace(System.err);
                            }
                        }

                        pool.shutdownNow();
                    }));
            pool.invokeAll(asList(consoleMessageReaderCallable,
                    chatMessageSenderCallable,
                    consoleMessageWriterCallable,
                    chatMessageReceiver));
        } catch (final UnknownHostException exception) {
            System.err.printf("Неизвестный host: %s\n", address);
        } catch (final IOException exception) {
            System.err.printf("Ошибка передачи данных (%s:%d): %s", address, port, exception.getMessage());
        } catch (final Exception exception) {
            System.err.println("Ошибка приложения:");
            exception.printStackTrace(System.err);
        }
    }

    private static String obtainUserName(final Scanner scanner) {
        System.out.print("Введите имя пользователя: ");
        return scanner.nextLine();
    }
}

