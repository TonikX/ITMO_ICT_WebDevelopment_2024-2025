package fourth;

import data.Constants;

import java.io.*;
import java.net.Socket;

public class Client {

    private Socket socket;

    private BufferedReader in;

    private BufferedWriter out;

    private BufferedReader userInput;

    private String nickname;

    public Client() {
        try {
            socket = new Socket(Constants.host, Constants.port);
            userInput = new BufferedReader(new InputStreamReader(System.in));
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            this.setNickname();
            new ReadMessage().start();
            new WriteMessage().start();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }


    }

    private void setNickname() {
        System.out.println("Введите имя пользователя");
        try {
            nickname = userInput.readLine();
            out.write("Пользователь с именем %s присоединился к чату \n".formatted(nickname));
            out.flush();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private class ReadMessage extends Thread {

        @Override
        public void run() {
            String message;
            try {
                while ((message = in.readLine()) != null) {
                    if (message.equalsIgnoreCase("exit")) {
                        leaveChat();
                        break;
                    }
                    System.out.println(message);
                }
            } catch (IOException e) {
                leaveChat();
            }
        }
    }

    public class WriteMessage extends Thread {

        @Override
        public void run() {
            String message;
            try {
                while ((message = userInput.readLine()) != null) {
                    if (message.equalsIgnoreCase("exit")) {
                        out.write(nickname + " вышел из чата. \n");
                        out.flush();
                        leaveChat();
                        break;
                    }
                    out.write("[%s]: %s \n".formatted(nickname, message));
                    out.flush();
                }
            } catch (IOException e) {
                leaveChat();
            }
        }
    }

    private void leaveChat() {
        if (!socket.isClosed()) {
            try {
                userInput.close();
                socket.close();
                in.close();
                out.close();
            } catch (IOException e) {
                System.out.println(e.getMessage());
            }
        }
    }

    public static void main(String[] args) {
        new Client();
    }
}
