public class Pair3 {
    private final String first;
    private final String second;

    public String getFirst() {
        return this.first;
    }

    public String getSecond() {
        return this.second;
    }

    public Pair3(String first, String second) {
        this.first = first;
        this.second = second;
    }

    @Override
    public String toString() {
        return "Pair{" +
                "first=" + first +
                ", second=" + second +
                '}';
    }
}
