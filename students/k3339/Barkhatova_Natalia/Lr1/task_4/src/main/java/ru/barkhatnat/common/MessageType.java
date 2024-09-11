package ru.barkhatnat.common;

import java.util.stream.Stream;

public enum MessageType {
    AUTH((byte) 0),
    CHAT((byte) 1);
    private final byte value;

    private MessageType(byte value) {
        this.value = value;
    }
    public byte getValue() {
        return value;
    }

    public static MessageType byValue(byte value) {
        return Stream.of(MessageType.values())
                .filter(item -> value == item.getValue())
                .findFirst()
                .orElseThrow(() -> new IllegalArgumentException("Unable to resolve message type with value=" + value));
    }
}
