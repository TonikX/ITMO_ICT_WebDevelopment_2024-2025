package ru.barkhatnat.common;

import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.Map;

public class MessageWriterImpl implements MessageWriter {

    private final DataOutputStream stream;

    public MessageWriterImpl(OutputStream stream) {
        this.stream = new DataOutputStream(stream);
    }

    @FunctionalInterface
    interface Writer<T extends Message> {
        void write(DataOutputStream stream, T message) throws IOException;
    }

    private static final Map<Class<? extends Message>, Writer<? extends Message>> CLASS_TO_WRITER =
            Map.<Class<? extends Message>, Writer<? extends Message>>of(AuthMessage.class,
                    (DataOutputStream stream, AuthMessage message) -> {
                        stream.writeByte(MessageType.AUTH.getValue());
                        stream.writeUTF(message.username());
                    },
                    ChatMessage.class,
                    (DataOutputStream stream, ChatMessage message) -> {
                        stream.writeByte(MessageType.CHAT.getValue());
                        stream.writeUTF(message.username());
                        stream.writeUTF(message.message());
                    });

    @Override
    public void write(final Message message) throws IOException {
        @SuppressWarnings("unchecked") final Writer<Message> writer = (Writer<Message>) CLASS_TO_WRITER.get(message.getClass());
        if (writer == null) {
            throw new IllegalArgumentException("Unknown message type: " + message);
        }
        writer.write(stream, message);
    }

    @Override
    public void close() throws IOException {
        stream.close();
    }
}
