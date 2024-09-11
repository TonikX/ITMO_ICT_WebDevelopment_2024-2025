package ru.barkhatnat.common;

import java.io.Closeable;
import java.io.IOException;
import java.io.OutputStream;

public interface MessageWriter extends Closeable {
    void write(Message message) throws IOException;

    static MessageWriter create(final OutputStream stream) {
        return new MessageWriterImpl(stream);
    }
}
