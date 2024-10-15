package fourth;

import java.io.*;
import java.net.Socket;

public class ClientHandler extends Thread {

    private final Socket socket;

    private BufferedReader in;

    private BufferedWriter out;

    public ClientHandler(Socket socket) throws IOException {
        this.socket = socket;
        in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));

        start();
    }

    @Override
    public void run() {
        String input;
        try {
            input = in.readLine();
            out.write(input + "\n");
            out.flush();

            while ((input = in.readLine()) != null) {
                if (input.equalsIgnoreCase("exit")) {
                    endChat();
                    break;
                }
                for (ClientHandler client : Server.clients) {
                    if (socket != client.socket) {
                        client.send(input);
                    }
                }
            }
        } catch (IOException e) {
            endChat();
        }
    }

    private void send(String message) {
        try {
            out.write(message + "\n");
            out.flush();
        } catch (IOException e) {
            endChat();
        }
    }

    private void endChat() {
        try {
            if (!socket.isClosed()) {
                socket.close();
                in.close();
                out.close();
            }
        } catch (IOException ignored) {
        }
    }
}
