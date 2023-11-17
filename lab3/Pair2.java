public class Pair2 {
    private final String token;
    private final Pair1 position;

    public String getFirst() {
        return this.token;
    }

    public Pair1 getSecond() {
        return this.position;
    }

    public Pair2(String token, Pair1 position) {
        this.token = token;
        this.position = position;
    }

    @Override
    public String toString() {
        return "Pair{" +
                "token=" + token +
                ", postion=" + position +
                '}';
    }
}
