package ru.barkhatnat.common;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Map;


public class MessageReaderImpl implements MessageReader {
    public final DataInputStream stream;

    public MessageReaderImpl(final InputStream stream) {
        this.stream = new DataInputStream(stream);

    }

    private static final Map<MessageType, Reader> TYPE_2_READER = Map.<MessageType, Reader>of(
            MessageType.AUTH,
            stream -> new AuthMessage(stream.readUTF()),
            MessageType.CHAT,
            stream -> new ChatMessage(stream.readUTF(), stream.readUTF())
    );
    @FunctionalInterface
    interface Reader {
        Message read(DataInputStream stream) throws IOException;
    }

    @Override
    public Message read() throws IOException {
        final MessageType messageType = MessageType.byValue(stream.readByte());
        final Reader reader = TYPE_2_READER.get(messageType);
        if (reader == null) {
            throw new IOException("Unknown message type: " + messageType);
        }
        return reader.read(stream);
    }

    @Override
    public void close() throws IOException {
        stream.close();
    }
}
