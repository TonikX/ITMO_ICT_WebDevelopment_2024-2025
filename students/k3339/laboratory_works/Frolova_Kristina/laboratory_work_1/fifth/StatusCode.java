package fifth;

public enum StatusCode {

    NOT_FOUND(404),

    BAD_REQUEST(400),

    OK(200);

    private int code;

    StatusCode(int code) {
        this.code = code;
    }

    public int getCode() {
        return code;
    }
}
