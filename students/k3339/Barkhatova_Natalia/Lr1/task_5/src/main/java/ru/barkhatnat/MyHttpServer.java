package ru.barkhatnat;

import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.util.HashMap;
import java.util.Map;

public class MyHttpServer {

    private final String host;
    private final int port;
    private final String name;
    private static final Map<String, String> grades = new HashMap<>();

    public MyHttpServer(String host, int port, String name) {
        this.host = host;
        this.port = port;
        this.name = name;
    }

    public void start() {
        try {
            HttpServer server = HttpServer.create(new InetSocketAddress(host, port), 0);
            System.out.println(name + " started on " + host + ":" + port);
            server.createContext("/grades", new MyHttpHandler(grades));
            server.setExecutor(null);
            server.start();
        } catch (IOException e) {
            System.err.println("Server failed to start: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        final String host = args.length > 0 ? args[0] : "localhost";
        final int port = args.length > 1 ? Integer.parseInt(args[1]) : 1234;
        final String name = args.length > 2 ? args[2] : "SimpleJavaHTTPServer";
        MyHttpServer server = new MyHttpServer(host, port, name);

        try {
            server.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
