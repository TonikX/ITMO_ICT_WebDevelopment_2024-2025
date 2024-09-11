package ru.barkhatnat.common;

import java.io.Closeable;
import java.io.IOException;
import java.io.InputStream;

public interface MessageReader extends Closeable {
    Message read() throws IOException;

    static MessageReader create(final InputStream stream) {
        return new MessageReaderImpl(stream);
    }
}
