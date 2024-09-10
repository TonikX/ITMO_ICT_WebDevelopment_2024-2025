package ru.barkhatnat.server;

import java.io.PrintWriter;

public class HttpResponseSender {
    private static final String HTTP_OK = "HTTP/1.1 200 OK";
    private static final String CONTENT_TYPE = "Content-Type: text/html; charset=UTF-8";

    public static void sendOkResponseWithContent(PrintWriter out, String htmlContent) {
        out.println(HTTP_OK);
        out.println(CONTENT_TYPE);
        out.println("Content-Length: " + htmlContent.length());
        out.println();
        out.print(htmlContent);
        out.flush();
    }
}
