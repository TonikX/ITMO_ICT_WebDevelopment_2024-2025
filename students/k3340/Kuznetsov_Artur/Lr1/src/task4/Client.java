package task4;

import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

public class Client {

    private Socket socket;
    private BufferedReader in;
    private BufferedWriter out;
    private BufferedReader userInput;
    private String nickname;

    public Client(String host, int serverPort) {
        try {
            socket = new Socket(host, serverPort);
            userInput = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
            in = new BufferedReader(new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
            out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8));

            this.setNickname();
            new ReadMessage().start();
            new WriteMessage().start();
        } catch (IOException e) {
            throw new RuntimeException("Ошибка подключения к серверу", e);
        }
    }

    private void setNickname() throws IOException {
        System.out.print("Введите ваше имя: ");
        nickname = userInput.readLine();
        out.write(nickname + " присоединился к чату.\n");
        out.flush();
    }

    private class ReadMessage extends Thread {
        @Override
        public void run() {
            String message;
            try {
                while ((message = in.readLine()) != null) {
                    System.out.println(message);
                }
            } catch (IOException e) {
                System.out.println("Соединение прервано: " + e.getMessage());
            }
        }
    }

    private class WriteMessage extends Thread {
        @Override
        public void run() {
            try {
                String message;
                while ((message = userInput.readLine()) != null) {
                    if (message.equalsIgnoreCase("exit")) {
                        out.write(nickname + " покинул чат.\n");
                        out.flush();
                        socket.close();
                        break;
                    }
                    out.write("[" + nickname + "]: " + message + "\n");
                    out.flush();
                }
            } catch (IOException e) {
                System.out.println("Ошибка отправки сообщения: " + e.getMessage());
            }
        }
    }

    public static void main(String[] args) {
        String host = "localhost";
        int serverPort = 8000;
        new Client(host, serverPort);
    }
}
